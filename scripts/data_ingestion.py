import pandas as pd
import os

folder = "data/raw"

files = sorted([f for f in os.listdir(folder) if f.endswith(".csv")])

print(f"\nTotal CSV Files Found: {len(files)}")

for file in files:
    print("\n" + "="*70)
    print("FILE:", file)

    path = os.path.join(folder, file)

    try:
        df = pd.read_csv(path)

        print("\nShape:")
        print(df.shape)

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nMissing Values:")
        print(df.isnull().sum())

    except Exception as e:
        print("ERROR:", e)