import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os


BASE = r"C:\Users\hp\MutualFundAnalysis"

PROCESSED = BASE + r"\data\processed"
RAW = BASE + r"\data\raw"

OUTPUT = BASE + r"\outputs"
CHART = BASE + r"\reports\charts"


os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(CHART, exist_ok=True)



# ======================
# LOAD DATA
# ======================

nav = pd.read_csv(
    PROCESSED + r"\nav_history_cleaned.csv"
)

perf = pd.read_csv(
    PROCESSED + r"\scheme_performance_cleaned.csv"
)

bench = pd.read_csv(
    RAW + r"\10_benchmark_indices.csv"
)



nav["date"] = pd.to_datetime(nav["date"])



# ======================
# DAILY RETURNS
# ======================

nav = nav.sort_values(
    ["amfi_code","date"]
)


nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)


print("Daily returns calculated")




# ======================
# CAGR
# ======================

cagr=[]


for fund,df in nav.groupby("amfi_code"):

    df=df.sort_values("date")


    start=df.iloc[0]["nav"]
    end=df.iloc[-1]["nav"]


    years=(
        df["date"].max()
        -
        df["date"].min()
    ).days / 365


    if years > 0:

        value=(end/start)**(1/years)-1

    else:

        value=np.nan


    cagr.append(
        [
            fund,
            value
        ]
    )



cagr_df=pd.DataFrame(
    cagr,
    columns=[
        "amfi_code",
        "cagr"
    ]
)




# ======================
# SHARPE RATIO
# ======================

sharpe=[]


for fund,df in nav.groupby("amfi_code"):


    r=df["daily_return"].dropna()


    value=(
        (r.mean()*252 - 0.065)
        /
        (r.std()*np.sqrt(252))
    )


    sharpe.append(
        [
            fund,
            value
        ]
    )


sharpe_df=pd.DataFrame(
    sharpe,
    columns=[
        "amfi_code",
        "sharpe_ratio"
    ]
)




# ======================
# SORTINO RATIO
# ======================

sortino=[]


for fund,df in nav.groupby("amfi_code"):


    r=df["daily_return"].dropna()


    downside=r[r<0]


    if len(downside)>0:

        value=(
            (r.mean()*252-0.065)
            /
            (downside.std()*np.sqrt(252))
        )

    else:

        value=np.nan


    sortino.append(
        [
            fund,
            value
        ]
    )


sortino_df=pd.DataFrame(
    sortino,
    columns=[
        "amfi_code",
        "sortino_ratio"
    ]
)




# ======================
# MAX DRAWDOWN
# ======================

drawdown=[]


for fund,df in nav.groupby("amfi_code"):


    running=df["nav"].cummax()


    dd=(
        df["nav"]/running - 1
    )


    drawdown.append(
        [
            fund,
            dd.min()
        ]
    )



dd_df=pd.DataFrame(
    drawdown,
    columns=[
        "amfi_code",
        "max_drawdown"
    ]
)




# ======================
# ALPHA AND BETA
# ======================


bench["date"] = pd.to_datetime(
    bench["date"]
)


# remove duplicate benchmark dates

bench = bench.drop_duplicates(
    subset="date"
)



benchmark = (
    bench
    .set_index("date")
    .iloc[:,-1]
    .pct_change()
)



alpha_beta=[]



for fund,df in nav.groupby("amfi_code"):


    temp = (
        df
        .set_index("date")
        .drop_duplicates()
    )


    merged = pd.concat(
        [
            temp["daily_return"],
            benchmark
        ],
        axis=1
    ).dropna()



    if len(merged)>10:


        result=linregress(
            merged.iloc[:,1],
            merged.iloc[:,0]
        )


        alpha=result.intercept*252

        beta=result.slope



        alpha_beta.append(
            [
                fund,
                alpha,
                beta
            ]
        )




alpha_beta_df=pd.DataFrame(
    alpha_beta,
    columns=[
        "amfi_code",
        "alpha",
        "beta"
    ]
)



alpha_beta_df.to_csv(
    OUTPUT+r"\alpha_beta.csv",
    index=False
)




# ======================
# FUND SCORECARD
# ======================


score=cagr_df.merge(
    sharpe_df,
    on="amfi_code"
)


score=score.merge(
    alpha_beta_df,
    on="amfi_code"
)


score=score.merge(
    dd_df,
    on="amfi_code"
)



score["return_rank"] = (
    score["cagr"]
    .rank(pct=True)
    *100
)


score["sharpe_rank"] = (
    score["sharpe_ratio"]
    .rank(pct=True)
    *100
)


score["alpha_rank"] = (
    score["alpha"]
    .rank(pct=True)
    *100
)


score["dd_rank"] = (
    (-score["max_drawdown"])
    .rank(pct=True)
    *100
)



score["fund_score"]=(

0.30*score["return_rank"]

+

0.25*score["sharpe_rank"]

+

0.20*score["alpha_rank"]

+

0.25*score["dd_rank"]

)



score=score.sort_values(
    "fund_score",
    ascending=False
)



score.to_csv(
    OUTPUT+r"\fund_scorecard.csv",
    index=False
)




# ======================
# TOP 5 FUND CHART
# ======================


top5 = score.head(5)["amfi_code"]



plt.figure(
    figsize=(12,6)
)



for fund in top5:


    df=nav[
        nav["amfi_code"]==fund
    ]


    plt.plot(
        df["date"],
        df["nav"],
        label=fund
    )



plt.title(
    "Top 5 Fund Performance"
)



plt.legend()



plt.savefig(
    CHART+r"\benchmark_comparison.png"
)



plt.close()



print("DAY 4 PERFORMANCE COMPLETED")