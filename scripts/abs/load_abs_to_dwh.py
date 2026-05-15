from scripts.shared.db import DB
from scripts.shared.load_util import load_table_to_dwh_incremental

SOURCE_DB = DB.ABS.value
SOURCE_SCHEMA = "public"
TARGET_SCHEMA = "bronze"


TABLES = [
    {
        "source_table": "accounts",
        "target_table": "abs_accounts",
    },
    {
        "source_table": "clients",
        "target_table": "abs_clients",
    },
    {
        "source_table": "transactions",
        "target_table": "abs_transactions",
    },
]

if __name__ == "__main__":
    for table in TABLES:
        load_table_to_dwh_incremental(
            source_db=SOURCE_DB,
            source_schema=SOURCE_SCHEMA,
            source_table=table["source_table"],
            target_schema=TARGET_SCHEMA,
            target_table=table["target_table"],
            watermark_column="updated_at",
        )