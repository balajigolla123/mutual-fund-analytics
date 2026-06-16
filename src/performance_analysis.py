"""
Performance analysis module
for Bluestock Mutual Fund Analytics project.
"""


import pandas as pd
import os


PROCESSED = "data/processed"
OUTPUT = "outputs"


os.makedirs(OUTPUT, exist_ok=True)



def performance_metrics():

    """
    Calculates mutual fund daily returns.
    """


    file_path = (
        f"{PROCESSED}/nav_history_cleaned.csv"
    )


    nav = pd.read_csv(file_path)


    nav["date"] = pd.to_datetime(
        nav["date"]
    )


    nav = nav.sort_values(
        ["amfi_code","date"]
    )


    nav["daily_return"] = (
        nav.groupby("amfi_code")["nav"]
        .pct_change()
    )


    nav.to_csv(
        f"{OUTPUT}/performance_results.csv",
        index=False
    )


    print("Daily returns calculated")

    print("DAY 4 PERFORMANCE COMPLETED")