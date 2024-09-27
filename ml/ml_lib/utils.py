import pandas as pd


def load_data(file_path_train, file_path_iab, cols=("video_id", "title", "description")):
    data = pd.read_csv(file_path_train)[list(cols)]
    taxonomy = pd.read_csv(file_path_iab)

    print(f"Data columns: {data.columns.tolist()}")
    print(f"Data head: \n{data.head(5)}")

    print(f"Taxonomy head: \n{taxonomy.head(5)}")
    print(f"Taxonomy columns: {taxonomy.columns.tolist()}")
    return data, taxonomy

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