import argparse
import pandas as pd
import numpy as np

from pathlib import Path


def main(input_file, output_dir, fraction, seed):
    np.random.seed(seed)  # Устанавливаем фиксированный seed

    # Чтение данных
    df = pd.read_csv(input_file)

    # Перемешивание данных
    df = df.sample(frac=1).reset_index(drop=True)  # перемешиваем все данные

    # Деление данных
    split_idx = int(fraction * len(df))
    df1 = df[:split_idx]
    df2 = df[split_idx:]

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Сохранение данных
    df1.to_csv(f"{output_dir}/train.csv", index=False)
    df2.to_csv(f"{output_dir}/val.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split DataFrame into two subsets.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output CSV files.")
    parser.add_argument("--fraction", type=float, required=True, help="Fraction of data for the first DataFrame, between 0 and 1.")
    parser.add_argument("--seed", type=int, required=True, help="Seed for random number generator.")

    args = parser.parse_args()

    main(args.input_file, args.output_dir, args.fraction, args.seed)
