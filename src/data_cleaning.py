import pandas as pd
import os


RAW = "../data/raw"
PROCESSED = "../data/processed"


os.makedirs(PROCESSED, exist_ok=True)


print("Starting Cleaning...")


# ==============================
# NAV HISTORY
# ==============================

print("\nCleaning NAV History")


nav = pd.read_csv(
    f"{RAW}/02_nav_history.csv"
)


print(nav.columns)


# date column detection

nav["date"] = pd.to_datetime(
    nav["date"],
    errors="coerce"
)


nav["nav"] = pd.to_numeric(
    nav["nav"],
    errors="coerce"
)


nav = nav.sort_values(
    ["amfi_code","date"]
)


nav["nav"] = (
    nav.groupby("amfi_code")["nav"]
    .ffill()
)


nav = nav.drop_duplicates()


nav = nav[
    nav["nav"] > 0
]


nav.to_csv(
    f"{PROCESSED}/nav_history_cleaned.csv",
    index=False
)


print(
    "NAV rows:",
    len(nav)
)



# ==============================
# TRANSACTIONS
# ==============================

print("\nCleaning Transactions")


txn = pd.read_csv(
    f"{RAW}/08_investor_transactions.csv"
)


print(txn.columns)



txn["transaction_type"] = (
    txn["transaction_type"]
    .astype(str)
    .str.upper()
    .str.strip()
)


txn["transaction_type"] = (
    txn["transaction_type"]
    .replace(
        {
        "LUMP SUM":"LUMPSUM",
        "REDEEM":"REDEMPTION"
        }
    )
)



txn["amount_inr"] = pd.to_numeric(
    txn["amount_inr"],
    errors="coerce"
)



txn = txn[
    txn["amount_inr"] > 0
]



txn.to_csv(
    f"{PROCESSED}/investor_transactions_cleaned.csv",
    index=False
)


print(
    "Transaction rows:",
    len(txn)
)



# ==============================
# PERFORMANCE
# ==============================


print("\nCleaning Performance")


perf = pd.read_csv(
    f"{RAW}/07_scheme_performance.csv"
)


print(perf.columns)



for col in perf.columns:

    if (
        "return" in col.lower()
        or
        "expense" in col.lower()
    ):

        perf[col] = pd.to_numeric(
            perf[col],
            errors="coerce"
        )



if "expense_ratio" in perf.columns:

    perf = perf[
        (perf["expense_ratio"] >= 0.1)
        &
        (perf["expense_ratio"] <= 2.5)
    ]



perf.to_csv(
    f"{PROCESSED}/scheme_performance_cleaned.csv",
    index=False
)


print(
    "Performance rows:",
    len(perf)
)



print("\nCLEANING COMPLETED SUCCESSFULLY")