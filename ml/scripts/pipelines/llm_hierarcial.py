from dataclasses import dataclass
import guidance
from tqdm import tqdm
import pathlib
import pandas as pd

from tqdm import tqdm

from guidance.models._model import ConstraintException
from guidance import system, user, assistant, select, zero_or_more, with_temperature
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator


from ml_lib.utils import load_data, create_nested_structure, truncate_string
from ml_lib.model_registry import load_model_hf, load_model_openrounter
from ml_lib.few_shot_rag import build_few_shot_index, make_retrieve_prompt, make_view_name_from_tags, join_tag_with_subtags

from typing import Optional


@dataclass
class VideoFeatures:
    video_id: str
    title: str
    description: str
    video_desc: Optional[str] = None
    s2t: Optional[str] = None

class VideoTagsPrediction(VideoFeatures):
    predicted_tags: list[str]


@dataclass
class _LevelCat:
    view_name: str
    taxonomy_name: str


def make_categories(categories: list[_LevelCat], all_good_cat=True, wrong_cat=False):
    # ллм не любят нолики
    all_good_cat_idx = None
    wrong_cat_idx = None
    starts_from=1
    p = "\n".join(f"{i}. {c.view_name.strip()}" for i, c in enumerate(categories, starts_from))
    if all_good_cat:
        all_good_cat_idx = len(categories) + starts_from + 1
        p += f"\n{all_good_cat_idx + starts_from}. Подходит большинство категорий / Доуточнения категории не требуется"
    if wrong_cat:
        wrong_cat_idx = len(categories) + starts_from + 1 + int(all_good_cat)
        p += f"\n{wrong_cat_idx + starts_from}. Ничего не подходит, категория была ошибочной"
    return p, all_good_cat_idx, wrong_cat_idx


def make_few_shot(video_features: VideoFeatures, tags_idx=None):
    vf = video_features
    delimeter = "\n---\n"
    additional_info = ""
    if vf.s2t:
        additional_info += f"Субтитры первых минут видео:{delimeter}{truncate_string(vf.s2t, 256)}{delimeter}\n"
    if vf.video_desc:
        additional_info += f"Описание видео по случайным кадрам:{delimeter}{truncate_string(vf.video_desc, 256)}{delimeter}\n"
    return f"""\
Информация о видео:
===
Название:{delimeter}{vf.title}{delimeter}

Описание:{delimeter}{vf.description}{delimeter}

{additional_info}\
===

Выбранные индексы категорий из списка вначале: \
""" + (
    ', '.join(map(lambda x: str(x+1), tags_idx)) 
if tags_idx is not None else "")


def remove_empty_lists(input_list):
    return [item for item in input_list if item != []]


def find_indices(list1, list2):
    indices = []
    element_to_indices = {element: index for index, element in enumerate(list2)}
    
    for element in list1:
        if element in element_to_indices:  # Проверяем, есть ли элемент в словаре.
            indices.append(element_to_indices[element])
    
    return indices


def predict_video(
    lm, 
    nested_taxonomy: dict[str, dict[str, list]], 
    video_features: VideoFeatures, 
    max_cats_at_time=2, 
    max_predict_level=3,
    debug=False,
    verbose=True,
    few_shot_index: Optional[VectorStoreIndex]=None,
    max_few_shots=3,
    # todo: later
    similarity_top_k=7,
) -> VideoTagsPrediction:
    verbose = verbose or debug
    vf = video_features
    predicted_tags = []
    level = 0

    while level < max_predict_level:
        categories_multiple = []  # type: list[list[_LevelCat]]
        if level == 0:
            categories_multiple.append((-1, [_LevelCat(t, t) for t in nested_taxonomy]))
        else:
            for i, predicted_t in enumerate(predicted_tags):
                d = nested_taxonomy
                prefix = None
                for t in predicted_t:
                    prefix = (f"{prefix}, " if prefix else "") + t
                    d = d[t]
                cats = [_LevelCat(f"{prefix} -> " + t, t) for t in d]
                if len(cats) != 0:
                    categories_multiple.append((i, cats))

        # всегда есть категория на 0 уровне
        all_good_cat = level!=0
        wrong_cat = level!=0
        # all_good_cat = False
        # wrong_cat = False
        for pred_i, categories in categories_multiple:  # type: list[_LevelCat]
            prompt_cat, all_good_cat_idx, wrong_cat_idx  = make_categories(
                categories, 
                all_good_cat=all_good_cat, 
                wrong_cat=wrong_cat
            )
            
            few_shot_prompts = []
            if few_shot_index is not None:
                filters = None
                if level > 0:
                    filters = MetadataFilters(
                        filters=[
                            MetadataFilter(
                                key='expand_tags',
                                value=join_tag_with_subtags(
                                    categories[0].view_name.split(' -> ')[:-1]
                                ),
                                operator=FilterOperator.CONTAINS
                            )
                        ]
                    )
                    print(f"{filters=}")

                few_shot_retriever = few_shot_index.as_retriever(
                    similarity_top_k=similarity_top_k,
                    filters=filters
                )
                few_shots = few_shot_retriever.retrieve(
                    make_retrieve_prompt(
                        vf.title, vf.description
                    )
                )
                # print(few_shots)
                top_few_shot_tag_idx = None
                for i, shot_node_with_score in enumerate(few_shots):
                    shot = shot_node_with_score.node
                    few_shot_tags_view_names = make_view_name_from_tags(shot.metadata['tags'], level+1)
                    list2lookup_tags = [c.view_name for c in categories]
                    # print(f"{i=} {few_shot_tags_view_names=}")
                    tag_idxs = find_indices(few_shot_tags_view_names, list2lookup_tags)
                    if i == 0:
                        top_few_shot_tag_idx = tag_idxs
                    if len(tag_idxs) != 0:
                        few_shot_prompts += [make_few_shot(VideoFeatures(
                            video_id=shot.metadata['video_id'],
                            title=shot.metadata['Название видео'],
                            description=shot.text,
                            video_desc=shot.metadata.get("Описание видео по 10 кадрам", None),
                            s2t=shot.metadata.get("Транскибация первых минут видео", None),
                        ), tags_idx=tag_idxs)]
                few_shot_prompts = few_shot_prompts[:max_few_shots] 
                
            few_shot_prompt = (
                "\nНиже примеры - как проставлются категории для похожих видео. " + 
                "Обрати внимание на количество категорий! " +
                "\n=====\n" +
                "\n--\n".join(few_shot_prompts) + 
                "\n=====\n\n" +
                "А теперь твоя очередь, ниже информация по целевому видео на категоризацию. " +
                ("Если ты видишь, что в большинстве примеров выбрана категория \"Массовая культура\" - выбери ее." if level == 0 else "")
            ) if len(few_shot_prompts) > 0 else ""
            
            max_retires = 1
            retry_cnt = max_retires
            retry = True
            pred_cats = []
            while retry and retry_cnt > 0:
                try:
                    lm_ = lm
                    with user():
                        lm_ += (
                            'Тебе нужно выбрать какие категории и подкатегории из списка подходят для видео на видеохостинге. '
                            'Ниже список категорий:\n'
                            f'{prompt_cat}\n\n'
                            # todo: make few shots
                            #####
                            f"{'Обрати внимание, что категорий может быть несколько (НЕ более двух)! ' if level==0 else ''}"
                            f"{'Это НЕ значит, что категории всегда должно быть две. ' if level==0 else ''}"
                            f"{'Если ты сомневаешься в количестве, обрати внимание на количество категорий у приведенных примеров. ' if len(few_shot_prompt)!=0 else ''}"
                            f"{'Обрати внимание, что категория может быть ТОЛЬКО одна! ' if level>0 else ''}"
                            f"{'Если ничего или большинство подходит - выбери соответствующую опцию. ' if all_good_cat else ''}"
                            'Ответ СРАЗУ начинай с номеров подходящих категорий через запятую, номера разделяй пробелом.\n'
                            f'{few_shot_prompt}\n'
                            f'{make_few_shot(vf)}\n'
                            # 'Выбранные номера категорий:'
                        ).strip()

                    choose_cats = list(range(len(categories)))
                    if all_good_cat_idx is not None:
                        choose_cats += [all_good_cat_idx]
                    if wrong_cat_idx is not None:
                        choose_cats += [wrong_cat_idx]
                    
                    with assistant():
                        # starts from 1
                        p = select(
                            [str(i+1) for i in choose_cats], list_append=True, name="pred_cats",
                        )
                        lm_ += with_temperature(
                            zero_or_more(p + select([", ", ","])) + p + select(["<|eot_id|>", ""]), 
                            # чтобы ретрай не отдавал нам то же самое
                            0 + (max_retires - retry_cnt)*0.1
                        )

                    if verbose:
                        print(lm_)
                    retry = False
                    pred_cats = lm_["pred_cats"]
                except ConstraintException:
                    retry = True
                    if top_few_shot_tag_idx is not None:
                        pred_cats = list(str(c) for c in top_few_shot_tag_idx)[:1]
                    
                except Exception as e:
                    retry = False
                    if debug:
                        print(
                            f"{vf.video_id=}",
                            f"{vf.title=}",
                        )
                        raise e

                    print(
                        f"{vf.video_id=}",
                        f"{vf.title=}",
                        f"{e =}",
                    )
                retry_cnt -= 1

            # Parse answer
            # level 1
            if pred_i == -1:
                for pred_cat_idx in set(pred_cats):
                    pred_cat_idx_ = pred_cat_idx[:-1] if "," in pred_cat_idx else pred_cat_idx
                    pred_tag = categories[int(pred_cat_idx_) - 1].taxonomy_name
                    predicted_tags.append([pred_tag])
            else:
                tmp = []
                set_pred_cats = set(pred_cats)
                    # start from = 1
                set_pred_cats = [int(t[:-1] if "," in t else t)-1 for t in set_pred_cats]
                print(f"{set_pred_cats=}")
                
                #  todo: <eot_id> generate
                if all_good_cat_idx in set_pred_cats:
                    tmp.append(predicted_tags[pred_i])
                elif wrong_cat_idx in set_pred_cats:
                    ...
                else:
                    # если ллм выбрала много категорий - стопаем ее
                    if len(set_pred_cats) <= max_cats_at_time:
                        for choose_cat_id in set_pred_cats:
                            pred_tag = categories[choose_cat_id].taxonomy_name
                            tmp.append(predicted_tags[pred_i] + [pred_tag])
                        predicted_tags[pred_i] = []
                        predicted_tags += tmp
            if verbose:
                print(f"{predicted_tags=}")


        predicted_tags = remove_empty_lists(predicted_tags)
        level += 1

    predicted_tags = remove_empty_lists(predicted_tags)
    return {
        "video_id": vf.video_id,
        "title": vf.title,
        "description": vf.description,
        "predicted_tags": [": ".join(l) for l in predicted_tags],
    }


def main(args):
    few_shot_index = build_few_shot_index(
        train_filepath_csv=args.file_path_train,
        model_name=args.few_shot_retriever_model,
        video_desc_dir=args.train_video_desc_dir,
        s2t_dir=args.train_s2t_dir,
        
    )
    # predict mode only
    data, taxonomy, pred_video_desc_dict, pred_s2t_dict = load_data(
        file_path_train=args.file_path_predict, 
        file_path_iab=args.file_path_iab,
        video_desc_dir=args.predict_video_desc_dir,
        s2t_dir=args.predict_s2t_dir,
    )
    pred_video_desc_dict = pred_video_desc_dict or {}
    pred_s2t_dict = pred_s2t_dict or {}
    nested_taxonomy = create_nested_structure(taxonomy)  # type: dict[str, dict[str, list]]
    if args.model_type == 'hf':
        lm = load_model_hf(args.hf_model_name)
    elif args.model_type == 'openrouter':
        lm = load_model_openrounter(args.openrouter_model_name)
    else:
        raise NotImplementedError(f"{args.model_type=}")
    with system():
        lm += "Ты большой эксперт в определении тематик видео по передаваеным тебе признакам. "

    results = []
    try:
        if not args.predict_all:
            print("===" * 4)
            print("prediction example (only 5 videos), pass PREDICT_ALL=True is want all")
            print("===" * 2)
            
            data = data.head()

        # Очистка файла с ошибками перед циклом
        with open("failed_predictions.log", "w") as f:
            pass

        for _, row in tqdm(data.iterrows(), total=data.shape[0]):
            max_retries = 1
            retry_cnt = 0
            prediction = None
            while prediction is None and retry_cnt < max_retries:
                video_id = row["video_id"]
                prediction = predict_video(
                    lm,
                    nested_taxonomy,
                    VideoFeatures(
                        video_id=video_id, title=row["title"], 
                        description=row["description"],
                        video_desc=pred_video_desc_dict.get(video_id),
                        s2t=pred_s2t_dict.get(video_id),
                    ),
                    verbose=True,
                    few_shot_index=few_shot_index,
                )
                if not prediction['predicted_tags']:
                    print(f"retry with {row['video_id']}")
                    retry_cnt += 1
            
            if not prediction['predicted_tags']:
                # Сохраняем лог в файл
                with open("failed_predictions.log", "a") as f:
                    f.write(f"Video ID: {row['video_id']}\n")
                    f.write(f"Title: {row['title']}\n")
                    f.write(f"Description: {row['description']}\n")
                    f.write(f"Video Desc: {pred_video_desc_dict.get(video_id)}\n")
                    f.write(f"S2T: {pred_s2t_dict.get(video_id)}\n")
                    f.write("\n")
            results.append(
                prediction
            )
            if not args.predict_all:
                print("SAMPLE id", row["video_id"])
                print("SAMPLE title", row["title"])
                print("PREDICTION", prediction["predicted_tags"])

    except KeyboardInterrupt as e:
        print('stop calc')

    sample_submission = pd.DataFrame(results)
    submission_file_dir = pathlib.Path(args.submission_file).parent
    submission_file_dir.mkdir(parents=True, exist_ok=True)
    sample_submission.to_csv(args.submission_file, index=False)


if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--submission_file",
        default=f"data/submits/baselinesample_submission_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
    )
    parser.add_argument("--file_path_train", default="data/train_dataset_tag_video/baseline/train_data_categories.csv")
    parser.add_argument("--file_path_predict", default="data/train_dataset_tag_video/baseline/train_data_categories.csv")
    parser.add_argument("--file_path_iab", default="data/train_dataset_tag_video/baseline/iab_taxonomy.csv")

    parser.add_argument("--train_video_desc_dir", default=None)
    parser.add_argument("--predict_video_desc_dir", default=None)
    
    parser.add_argument("--train_s2t_dir", default=None)
    parser.add_argument("--predict_s2t_dir", default=None)

    # NousResearch/Hermes-3-Llama-3.2-3B
    
    # few shot embedder
    parser.add_argument("--few_shot_retriever_model", default="intfloat/multilingual-e5-large")
    parser.add_argument("--few_shot_retriever_top_k", default=5)
    
    
    # llm
    parser.add_argument("--model-type", type=str, default="hf")
    parser.add_argument("--openrouter-model-name", type=str, default="meta-llama/llama-3.1-70b-instruct")
    parser.add_argument("--hf-model-name", type=str, default="unsloth/Llama-3.2-1B-Instruct")
    
    
    parser.add_argument("--predict-all", action="store_true", default=False)
    parser.add_argument("--debug", action="store_true", default=False)

    # parser.add_argument('--output', type=str, default='output.txt')
    args = parser.parse_args()
    main(args)
