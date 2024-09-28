import argparse
import pandas as pd
import re

from pathlib import Path


def transform_dataframe(df):
    rows = []
    for _, row in df.iterrows():
        video_id = row["video_id"]
        tags = row["tags"].split(", ")
        for tag in tags:
            levels = re.split(r":|\t", tag)
            while len(levels) < 3:
                levels.append("")
            rows.append([video_id] + levels)

    transformed_df = pd.DataFrame(rows, columns=["video_id", "level1", "level2", "level3"])
    for l in ["level1", "level2", "level3"]:
        transformed_df[l] = transformed_df[l].str.strip()
    return transformed_df



def generate_unique_levels_dataframe(df, threshold=0.05, min_samples=2):
    # Подсчет уникальных комбинаций уровней
    unique_levels = df[["level1", "level2", "level3"]].drop_duplicates()

    # Фильтрация уровней
    def filter_levels(column_name):
        counts = df[column_name].value_counts()
        total_samples = counts.sum()
        to_keep = counts[counts >= max(threshold * total_samples, min_samples)].index
        return to_keep

    level2_to_keep = filter_levels("level2")
    level3_to_keep = filter_levels("level3")

    # Фильтрация DataFrame с уникальными уровнями
    filtered_levels = unique_levels[
        (unique_levels["level2"].isin(level2_to_keep)) | (unique_levels["level3"].isin(level3_to_keep))
    ]

    return filtered_levels


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some file paths.')
    parser.add_argument('--train_csv_path', type=str, required=True, help='Path to the train data CSV file')
    parser.add_argument('--save_new_taxonomy_path', type=str, required=True, help='Path to save new taxonomy CSV file')
    parser.add_argument('--class_drop_threshold', type=float, required=False, default=0.05)
    parser.add_argument('--class_min_samples', type=int, required=False, default=2)
    
    args = parser.parse_args()
    
    train_csv_path = args.train_csv_path
    save_new_taxonomy_path = args.save_new_taxonomy_path
    
    Path(save_new_taxonomy_path).parent.mkdir(parents=True, exist_ok=True)

    train_df = pd.read_csv(
        train_csv_path
    )
    train_df.dropna(subset=("tags"), inplace=True)
    target_parsed_df = transform_dataframe(df=train_df)
    target_parsed_df["empty_levels"] = target_parsed_df.apply(
        lambda row: int(row["level2"] == "") + int(row["level3"] == ""), axis=1
    )
    result_df = generate_unique_levels_dataframe(
        target_parsed_df, 
        threshold=args.class_drop_threshold,
        min_samples=args.class_min_samples,
    )
    # result_df.groupby("level1")["level2"].count().sort_values(ascending=False).to_frame()
    
    result_df.columns = ['Уровень 1 (iab)', 'Уровень 2 (iab)', 'Уровень 3 (iab)']
    result_df.to_csv(save_new_taxonomy_path, index=False)

