"""
Master execution script for Bluestock Mutual Fund Analytics.
Runs complete ETL pipeline.
"""

from src.data_cleaning import clean_data
from src.eda_analysis import perform_eda
from src.performance_analysis import performance_metrics


def main():

    print("Starting pipeline")

    clean_data()

    perform_eda()

    performance_metrics()

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()