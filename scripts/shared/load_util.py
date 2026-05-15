import pandas as pd

from scripts.shared.db import get_engine, DB

from sqlalchemy import text


def get_last_loaded_at(source_name: str):
    dwh_engine = get_engine(DB.DWH.value)

    query = text("""
        SELECT last_loaded_at
        FROM metadata.etl_watermarks
        WHERE source_name = :source_name
    """)

    with dwh_engine.connect() as conn:
        result = conn.execute(query, {"source_name": source_name}).fetchone()

    if result is None:
        return "1900-01-01 00:00:00"

    return result[0]


def update_watermark(source_name: str, last_loaded_at):
    dwh_engine = get_engine(DB.DWH.value)

    query = text("""
        INSERT INTO metadata.etl_watermarks (source_name, last_loaded_at)
        VALUES (:source_name, :last_loaded_at)
        ON CONFLICT (source_name)
        DO UPDATE SET last_loaded_at = EXCLUDED.last_loaded_at
    """)

    with dwh_engine.begin() as conn:
        conn.execute(
            query,
            {
                "source_name": source_name,
                "last_loaded_at": last_loaded_at,
            }
        )


def load_table_to_dwh_incremental(
    source_db: str,
    source_schema: str,
    source_table: str,
    target_schema: str,
    target_table: str,
    watermark_column: str = "updated_at",
):
    source_name = f"{source_db}_{source_table}"

    source_engine = get_engine(source_db)
    dwh_engine = get_engine(DB.DWH.value)

    last_loaded_at = get_last_loaded_at(source_name)

    query = f"""
    SELECT *
    FROM {source_schema}.{source_table}
    WHERE {watermark_column} > '{last_loaded_at}'
    """

    df = pd.read_sql(query, source_engine)

    if df.empty:
        print(f"No new rows for {source_name}")
        return

    print(f"Loaded {len(df)} new/updated rows from {source_schema}.{source_table}")

    df.to_sql(
        name=target_table,
        schema=target_schema,
        con=dwh_engine,
        if_exists="append",
        index=False,
    )

    new_watermark = df[watermark_column].max()
    update_watermark(source_name, new_watermark)

    print(f"Updated watermark for {source_name}: {new_watermark}")

def load_dataframe_incremental(
    df: pd.DataFrame,
    source_name: str,
    target_schema: str,
    target_table: str,
    watermark_column: str,
) -> None:
    dwh_engine = get_engine(DB.DWH.value)

    last_loaded_at = get_last_loaded_at(source_name)

    df[watermark_column] = pd.to_datetime(df[watermark_column])
    last_loaded_at = pd.to_datetime(last_loaded_at)

    df_new = df[df[watermark_column] > last_loaded_at]

    if df_new.empty:
        print(f"No new rows for {source_name}")
        return

    df_new.to_sql(
        name=target_table,
        schema=target_schema,
        con=dwh_engine,
        if_exists="append",
        index=False,
    )

    new_watermark = df_new[watermark_column].max()
    update_watermark(source_name, new_watermark)

    print(f"Loaded {len(df_new)} rows into {target_schema}.{target_table}")
    print(f"Updated watermark for {source_name}: {new_watermark}")