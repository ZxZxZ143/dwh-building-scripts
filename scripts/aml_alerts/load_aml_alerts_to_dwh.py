import pandas as pd

from scripts.shared.load_util import load_dataframe_incremental

CSV_PATH = "/opt/airflow/data/csv/aml_alerts.csv"

if __name__ == "__main__":
    df = pd.read_csv(CSV_PATH)

    load_dataframe_incremental(
        df=df,
        source_name="aml_alerts_csv",
        target_schema="bronze",
        target_table="aml_alerts",
        watermark_column="alert_date",
    )