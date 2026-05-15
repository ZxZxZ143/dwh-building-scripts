import json

import pandas as pd

from scripts.shared.load_util import load_dataframe_incremental

JSON_FILES = [
    {
        "path": "/opt/airflow/data/json/dbo/dbo_events.json",
        "source_name": "dbo_events_json",
        "target_table": "dbo_events",
        "watermark_column": "event_time",
    },
    {
        "path": "/opt/airflow/data/json/dbo/dbo_sessions.json",
        "source_name": "dbo_sessions_json",
        "target_table": "dbo_sessions",
        "watermark_column": "login_time",
    },
]


def read_json(path: str) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return pd.json_normalize(data)


if __name__ == "__main__":
    for item in JSON_FILES:
        df = read_json(item["path"])

        load_dataframe_incremental(
            df=df,
            source_name=item["source_name"],
            target_schema="bronze",
            target_table=item["target_table"],
            watermark_column=item["watermark_column"],
        )