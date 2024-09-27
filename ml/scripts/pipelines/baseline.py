import pandas as pd
from sentence_transformers import SentenceTransformer
import json
from tqdm.autonotebook import tqdm
import numpy as np
import faiss
from pathlib import Path
from datetime import datetime
import argparse
from datetime import datetime


def load_data(file_path_train, file_path_iab):
    data = pd.read_csv(file_path_train)[["video_id", "title"]]
    taxonomy = pd.read_csv(file_path_iab)

    print(f"Data columns: {data.columns.tolist()}")
    print(f"Data head: \n{data.head(5)}")

    print(f"Taxonomy head: \n{taxonomy.head(5)}")
    print(f"Taxonomy columns: {taxonomy.columns.tolist()}")
    return data, taxonomy


def load_model():
    model = SentenceTransformer(
        "DeepPavlov/rubert-base-cased-sentence",
    )
    dim = 768  # размер вектора эмбеддинга
    return model, dim


def get_tags(model, taxonomy):
    tags = {}
    for i, row in tqdm(taxonomy.iterrows()):
        if isinstance(row["Уровень 1 (iab)"], str):
            tags[row["Уровень 1 (iab)"]] = (
                model.encode(row["Уровень 1 (iab)"], convert_to_tensor=True)
                .cpu()
                .numpy()
            )  # .tolist()
        if isinstance(row["Уровень 2 (iab)"], str):
            tags[row["Уровень 1 (iab)"] + ": " + row["Уровень 2 (iab)"]] = (
                model.encode(
                    row["Уровень 1 (iab)"] + ": " + row["Уровень 2 (iab)"],
                    convert_to_tensor=True,
                )
                .cpu()
                .numpy()
            )  # .tolist()
        if isinstance(row["Уровень 3 (iab)"], str):
            tags[
                row["Уровень 1 (iab)"]
                + ": "
                + row["Уровень 2 (iab)"]
                + ": "
                + row["Уровень 3 (iab)"]
            ] = (
                model.encode(
                    row["Уровень 1 (iab)"]
                    + ": "
                    + row["Уровень 2 (iab)"]
                    + ": "
                    + row["Уровень 3 (iab)"],
                    convert_to_tensor=True,
                )
                .cpu()
                .numpy()
            )  # .tolist()
    return tags


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--submission_file",
        default=f"data/submits/baselinesample_submission_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
    )
    parser.add_argument(
        "--file_path_train",
        default="data/train_dataset_tag_video/baseline/train_data_categories.csv",
    )
    parser.add_argument(
        "--file_path_iab",
        default="data/train_dataset_tag_video/baseline/iab_taxonomy.csv",
    )
    parser.add_argument("--generate-random", action="store_true", default=False)

    args = parser.parse_args()

    submission_file = args.submission_file
    data, taxonomy = load_data(
        file_path_train=args.file_path_train, file_path_iab=args.file_path_iab
    )
    model, dim = load_model()

    data["title_vector"] = data["title"].apply(
        lambda l: model.encode(l, convert_to_tensor=True).cpu().numpy()
    )

    tags = get_tags(model, taxonomy)
    tags_list = list(tags.keys())
    vectors = np.array(list(tags.values()))

    index = faiss.index_factory(dim, "Flat", faiss.METRIC_INNER_PRODUCT)
    index.add(vectors)
    print(f"Index size: {index.ntotal}")

    print(f"Data shape: {data.shape}")
    print(f"Data head: \n{data.head(5)}")

    print(f"Tags shape: {len(tags_list)}")

    if not args.generate_random:
        print("===" * 4)
        print("prediction example")
        print("===" * 2)

        topn = 3
        scores, predictions = index.search(
            np.array(data["title_vector"].to_list()[:10]), topn
        )

        for j, i in enumerate(predictions):
            print("SCORES", scores[j])
            print("PREDICTION_by_title", np.array(tags_list)[predictions[j]])
            print("SAMPLE", data["title"].to_list()[:10][j])
            print("\n")
        print("===" * 4)

    print("create submission file")
    topn = 1
    sample_submission = pd.DataFrame(
        data=data["video_id"].to_list(), columns=["video_id"]
    )
    sample_submission["predicted_tags"] = np.nan
    sample_submission["predicted_tags"] = sample_submission["predicted_tags"].astype(
        "object"
    )

    for i, row in data.iterrows():
        if args.generate_random:
            predictions = np.random.randint(0, len(tags_list), size=(1, topn))
            scores = np.random.rand(1, topn)
        else:
            scores, predictions = index.search(np.array([row["title_vector"]]), topn)
        index_i = sample_submission[sample_submission.video_id == row.video_id].index
        sample_submission.at[index_i[0], "predicted_tags"] = [
            tags_list[predictions[0][0]]
        ]  # вытаскиваем предсказание из

    import pathlib

    submission_file_dir = pathlib.Path(submission_file).parent
    submission_file_dir.mkdir(parents=True, exist_ok=True)
    sample_submission.to_csv(submission_file, index=False)
