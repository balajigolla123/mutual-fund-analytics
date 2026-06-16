"""
Exploratory Data Analysis module
for Bluestock Mutual Fund Analytics project.
"""


import pandas as pd
import os


PROCESSED = "data/processed"
OUTPUT = "outputs"


os.makedirs(OUTPUT, exist_ok=True)



def perform_eda():

    """
    Performs EDA on cleaned NAV data.
    """

    file_path = (
        f"{PROCESSED}/nav_history_cleaned.csv"
    )


    nav = pd.read_csv(file_path)


    summary = nav.describe()


    summary.to_csv(
        f"{OUTPUT}/eda_summary.csv",
        index=False
    )


    print("EDA summary generated")

    print("DAY 3 EDA COMPLETED")