import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os


BASE = r"C:\Users\hp\MutualFundAnalysis"

RAW = BASE + r"\data\raw"
PROCESSED = BASE + r"\data\processed"

CHART = BASE + r"\reports\charts"

os.makedirs(CHART, exist_ok=True)


# LOAD DATA

nav = pd.read_csv(PROCESSED+r"\nav_history_cleaned.csv")
txn = pd.read_csv(PROCESSED+r"\investor_transactions_cleaned.csv")
perf = pd.read_csv(PROCESSED+r"\scheme_performance_cleaned.csv")

aum = pd.read_csv(RAW+r"\03_aum_by_fund_house.csv")
sip = pd.read_csv(RAW+r"\04_monthly_sip_inflows.csv")
category = pd.read_csv(RAW+r"\05_category_inflows.csv")
folio = pd.read_csv(RAW+r"\06_industry_folio_count.csv")
portfolio = pd.read_csv(RAW+r"\09_portfolio_holdings.csv")



# 1 NAV TREND

nav["date"]=pd.to_datetime(nav["date"])

fig=px.line(
    nav,
    x="date",
    y="nav",
    color="amfi_code",
    title="NAV Trend 2022-2026"
)

fig.write_html(CHART+r"\nav_trend.html")



# 2 AUM BAR

fig=px.bar(
    aum,
    x=aum.columns[0],
    y=aum.columns[-1],
    color=aum.columns[1],
    title="Fund House AUM Growth"
)

fig.write_html(CHART+r"\aum_growth.html")



# 3 SIP TREND

sip.plot(
    figsize=(10,5)
)

plt.title(
"Monthly SIP Inflow Trend"
)

plt.savefig(CHART+r"\sip_trend.png")

plt.close()



# 4 CATEGORY HEATMAP

pivot=category.pivot_table(
    index=category.columns[0],
    columns=category.columns[1],
    values=category.columns[-1]
)


plt.figure(figsize=(12,6))

sns.heatmap(
    pivot
)

plt.title(
"Category Inflow Heatmap"
)

plt.savefig(CHART+r"\category_heatmap.png")

plt.close()



# 5 AGE DISTRIBUTION

txn["age_group"].value_counts().plot(
kind="pie",
autopct="%1.1f%%"
)

plt.title(
"Investor Age Distribution"
)

plt.savefig(CHART+r"\age_distribution.png")

plt.close()



# 6 SIP BY AGE

plt.figure(figsize=(10,5))

sns.boxplot(
data=txn,
x="age_group",
y="amount_inr"
)

plt.savefig(
CHART+r"\sip_age_boxplot.png"
)

plt.close()



# 7 GENDER

sns.countplot(
data=txn,
x="gender"
)

plt.savefig(
CHART+r"\gender_split.png"
)

plt.close()



# 8 STATE SIP

state=txn.groupby(
"state"
)["amount_inr"].sum()


state.plot(
kind="barh",
figsize=(10,6)
)

plt.title(
"SIP Amount By State"
)

plt.savefig(
CHART+r"\state_sip.png"
)

plt.close()



# 9 CITY TIER

txn["city_tier"].value_counts().plot(
kind="pie",
autopct="%1.1f%%"
)

plt.title(
"T30 B30 Distribution"
)

plt.savefig(
CHART+r"\city_tier.png"
)

plt.close()



# 10 FOLIO

plt.figure(figsize=(10,5))

plt.plot(
folio.iloc[:,0],
folio.iloc[:,-1]
)

plt.title(
"Folio Growth"
)

plt.savefig(
CHART+r"\folio_growth.png"
)

plt.close()



# 11 CORRELATION


nav_table=nav.pivot(
index="date",
columns="amfi_code",
values="nav"
)


returns=nav_table.pct_change()


corr=returns.iloc[:,:10].corr()


plt.figure(figsize=(10,8))

sns.heatmap(
corr,
annot=True
)


plt.title(
"NAV Return Correlation"
)

plt.savefig(
CHART+r"\correlation.png"
)

plt.close()



# 12 SECTOR ALLOCATION


portfolio["weight_pct"] = pd.to_numeric(
    portfolio["weight_pct"],
    errors="coerce"
)


sector = (
    portfolio
    .groupby("sector")["weight_pct"]
    .sum()
)


sector = sector[
    sector > 0
]


plt.figure(figsize=(8,8))


sector.plot(
    kind="pie",
    autopct="%1.1f%%"
)


plt.title(
"Sector Allocation"
)


plt.ylabel("")


plt.savefig(
CHART+r"\sector_allocation.png"
)


plt.close()



print("Sector chart completed")
print("DAY 3 EDA COMPLETED")