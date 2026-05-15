from scripts.shared.db import DB
from scripts.shared.load_util import load_table_to_dwh_incremental

SOURCE_DB = DB.LOAN_SYSTEM.value
SOURCE_SCHEMA = "public"
TARGET_SCHEMA = "bronze"


TABLES = [
    {
        "source_table": "loan_agreements",
        "target_table": "loan_system_loan_agreements",
    },
    {
        "source_table": "loan_applications",
        "target_table": "loan_system_loan_applications",
    },
    {
        "source_table": "payment_schedule",
        "target_table": "loan_system_payment_schedule",
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