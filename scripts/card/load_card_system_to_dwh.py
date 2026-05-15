from scripts.shared.db import DB
from scripts.shared.load_util import load_table_to_dwh_incremental

SOURCE_DB = DB.CARD_PROCESSING.value
SOURCE_SCHEMA = "public"
TARGET_SCHEMA = "bronze"


TABLES = [
    {
        "source_table": "authorizations",
        "target_table": "card_processing_authorizations",
    },
    {
        "source_table": "cards",
        "target_table": "card_processing_cards",
    },
    {
        "source_table": "clearing_transactions",
        "target_table": "card_processing_clearing_transactions",
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