from dataclasses import dataclass
import guidance
from tqdm import tqdm
import pathlib
import pandas as pd

from guidance import system, user, assistant, select, zero_or_more, at_most_n_repeats

from ml_lib.utils import load_data, create_nested_structure
from ml_lib.model_registry import load_model_hf


@dataclass
class VideoFeatures:
    video_id: str
    title: str
    description: str


class VideoTagsPrediction(VideoFeatures):
    predicted_tags: list[str]


@dataclass
class _LevelCat:
    view_name: str
    taxonomy_name: str


def make_categories(categories: list[_LevelCat], empty_cat=True):
    # ллм не любят нолики
    p = "\n".join(f"{i}. {c.view_name.strip()}" for i, c in enumerate(categories, 1))
    if empty_cat:
        p += f"\n{len(categories) + 2}. Подходит большинство категорий"
    return p


def make_few_shot(video_features):
    vf = video_features
    return f"""\
Название:
---
{vf.title}
---

Описание:
---
{vf.description}
---
"""


def remove_empty_lists(input_list):
    return [item for item in input_list if item != []]


def predict_video(
    lm, nested_taxonomy: dict[str, dict[str, list]], video_features: VideoFeatures, max_cats_at_time=3, verbose=True
) -> VideoTagsPrediction:
    vf = video_features
    predicted_tags = []
    level = 0

    while level < 3:
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
        # empty_cat = level!=0
        empty_cat = False
        for pred_i, categories in categories_multiple:  # type: list[_LevelCat]
            lm_ = lm
            with user():
                lm_ += (
                    'Тебе нужно выбрать какие категории и подкатегории (хотя бы одна) из списка подходят для видео на видеохостинге. '
                    'Ниже список категорий:\n'
                    f'{make_categories(categories, empty_cat=empty_cat)}\n\n'
                    # todo: make few shots
                    #####
                    'Вот информация по видео на видеохостинге:\n'
                    '===\n'
                    f'{make_few_shot(vf)}\n'
                    '===\n'
                    # f"{'Обрати внимание, что лучше выбрать несколько категорий (не более трех), чем одну! ' if level==0 else ''}"
                    # f"{'Обрати внимание, что категорий может быть несколько! ' if level>0 else ''}"
                    'Обрати внимание, что категорий может быть несколько! '
                    f"{'Если подходит большинство - выбери соответствующую опцию. ' if empty_cat else ''}"
                    'Ответ СРАЗУ начинай с номеров подходящих категорий через запятую:'
                ).strip()

            with assistant():
                p = select(
                    [str(i) for i in range(1, len(categories) + 1 + int(empty_cat))], list_append=True, name="pred_cats"
                )
                lm_ += at_most_n_repeats(p + ", ", n_repeats=max_cats_at_time - 1) + p

            if verbose:
                print(lm_)
            # Parse answer
            # level 1
            if pred_i == -1:
                for pred_cat_idx in set(lm_["pred_cats"]):
                    pred_cat_idx_ = pred_cat_idx[:-1] if "," in pred_cat_idx else pred_cat_idx
                    pred_tag = categories[int(pred_cat_idx_) - 1].taxonomy_name
                    predicted_tags.append([pred_tag])
            else:
                tmp = []
                set_pred_cats = set(lm_["pred_cats"])
                # если ллм выбрала много категорий - стопаем ее
                if len(set_pred_cats) < 3:
                    for pred_cat_idx in set_pred_cats:
                        pred_cat_idx_ = pred_cat_idx[:-1] if "," in pred_cat_idx else pred_cat_idx
                        pred_tag = categories[int(pred_cat_idx_) - 1].taxonomy_name
                        tmp.append(predicted_tags[pred_i] + [pred_tag])
                    predicted_tags[pred_i] = []
                    predicted_tags += tmp
            if verbose:
                print(f"{predicted_tags=}")

        predicted_tags = remove_empty_lists(predicted_tags)
        level += 1

    return {
        "video_id": vf.video_id,
        "title": vf.title,
        "description": vf.description,
        "predicted_tags": [": ".join(l) for l in predicted_tags],
    }


def main(args):
    data, taxonomy = load_data(file_path_train=args.file_path_train, file_path_iab=args.file_path_iab)
    nested_taxonomy = create_nested_structure(taxonomy)  # type: dict[str, dict[str, list]]

    lm = load_model_hf(args.hf_model_name)
    with system():
        lm += "Ты большой эксперт в определении тематик видео по передаваеным тебе признакам. "

    print("===" * 4)
    print("prediction example")
    print("===" * 2)

    if not args.predict_all:
        for _, row in data.head(2).iterrows():
            prediction = predict_video(
                lm,
                nested_taxonomy,
                VideoFeatures(video_id=row["video_id"], title=row["title"], description=row["description"]),
            )

            print("SAMPLE id", row["video_id"])
            print("SAMPLE title", row["title"])
            print("PREDICTION", prediction["predicted_tags"])
            print("\n")
        print("===" * 4)

    else:
        results = []
        for _, row in tqdm(data.iterrows(), total=data.shape[0]):
            results.append(
                predict_video(
                    lm,
                    nested_taxonomy,
                    VideoFeatures(
                        video_id=row["video_id"], title=row["title"], 
                        description=row["description"]
                    ),
                    verbose=True,
                )
            )

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
    parser.add_argument("--file_path_iab", default="data/train_dataset_tag_video/baseline/iab_taxonomy.csv")

    # NousResearch/Hermes-3-Llama-3.2-3B
    parser.add_argument("--hf-model-name", type=str, default="unsloth/Llama-3.2-1B-Instruct")
    parser.add_argument("--predict-all", action="store_true", default=False)

    # parser.add_argument('--output', type=str, default='output.txt')
    args = parser.parse_args()
    main(args)
