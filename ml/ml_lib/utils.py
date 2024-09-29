import json
import os
import pandas as pd

def truncate_string(s, max_length):
    """
    Обрезает строку до максимальной длины.

    Args:
        s (str): Исходная строка.
        max_length (int): Максимальная длина строки.

    Returns:
        str: Обрезанная строка.
    """
    if len(s) > max_length:
        return s[:max_length]
    return s

def json_dir_to_dict(directory):
    result = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            id = os.path.splitext(filename)[0]
            with open(os.path.join(directory, filename), 'r') as f:
                data = json.load(f)
                result[id] = data['content']
    return result

def text_dir_to_dict(directory):
    result = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            id = os.path.splitext(filename)[0]
            with open(os.path.join(directory, filename), 'r') as f:
                result[id] = f.read()
    return result

def load_data(
    file_path_train, file_path_iab, 
    cols=("video_id", "title", "description"),
    s2t_dir=None,
    video_desc_dir=None,
):
    data = pd.read_csv(file_path_train)[list(cols)]
    taxonomy = pd.read_csv(file_path_iab)
    
    s2t_dict = None
    video_desc_dict = None
    if s2t_dir:
        s2t_dict = text_dir_to_dict(s2t_dir)
        s2t_dict = {k: truncate_string(v, 256) for k, v in s2t_dict.items()}
        
    if video_desc_dir:
        video_desc_dict = json_dir_to_dict(video_desc_dir)

    print(f"Data columns: {data.columns.tolist()}")
    print(f"Data head: \n{data.head(5)}")

    print(f"Taxonomy head: \n{taxonomy.head(5)}")
    print(f"Taxonomy columns: {taxonomy.columns.tolist()}")
    return data, taxonomy, video_desc_dict, s2t_dict


def create_nested_structure(df):
    level_one = {}

    for _, row in df.iterrows():
        lvl1, lvl2, lvl3 = (
            row['Уровень 1 (iab)'], 
            row['Уровень 2 (iab)'], 
            row['Уровень 3 (iab)']
        )

        # Уровень 1
        if pd.isna(lvl1):
            continue

        lvl1 = lvl1.strip()
        if lvl1 not in level_one:
            level_one[lvl1] = {}

        # Уровень 2
        if pd.notna(lvl2):
            lvl1 = lvl1.strip()
            lvl2 = lvl2.strip()
            if lvl2 not in level_one[lvl1]:
                level_one[lvl1][lvl2] = []

            lvl2 = lvl2.strip()
            if pd.notna(lvl3):
                lvl3 = lvl3.strip()
                # Уровень 3
                if lvl3 not in level_one[lvl1][lvl2]:
                    level_one[lvl1][lvl2].append(lvl3)

    return level_one