from __future__ import annotations

import os
from enum import Enum

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv("/opt/airflow/.env")


class DB(Enum):
    ABS = "abs"
    LOAN_SYSTEM = "loan_system"
    CARD_PROCESSING = "card_processing"
    DWH = "dwh"


def build_database_url(prefix: str) -> URL:
    host = os.getenv(f"{prefix}_HOST", "host.docker.internal")
    port = int(os.getenv(f"{prefix}_PORT", 5432))

    db_name = os.getenv(f"{prefix}_DB")
    user = os.getenv(f"{prefix}_USER")
    password = os.getenv(f"{prefix}_PASSWORD")

    return URL.create(
        drivername="postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=port,
        database=db_name,
    )


DB1_URL = build_database_url("DB1")
engine_db1 = create_engine(
    DB1_URL,
    echo=False,
    future=True,
)
SessionLocalDB1 = sessionmaker(
    bind=engine_db1,
    autoflush=False,
    autocommit=False,
    future=True,
)


DB2_URL = build_database_url("DB2")
engine_db2 = create_engine(
    DB2_URL,
    echo=False,
    future=True,
)
SessionLocalDB2 = sessionmaker(
    bind=engine_db2,
    autoflush=False,
    autocommit=False,
    future=True,
)


DB3_URL = build_database_url("DB3")
engine_db3 = create_engine(
    DB3_URL,
    echo=False,
    future=True,
)
SessionLocalDB3 = sessionmaker(
    bind=engine_db3,
    autoflush=False,
    autocommit=False,
    future=True,
)


DWH_URL = build_database_url("DWH")
engine_dwh = create_engine(
    DWH_URL,
    echo=False,
    future=True,
)
SessionLocalDWH = sessionmaker(
    bind=engine_dwh,
    autoflush=False,
    autocommit=False,
    future=True,
)


ENGINES = {
    "abs": engine_db1,
    "loan_system": engine_db2,
    "card_processing": engine_db3,
    "dwh": engine_dwh,
}


SESSIONS = {
    "abs": SessionLocalDB1,
    "loan_system": SessionLocalDB2,
    "card_processing": SessionLocalDB3,
    "dwh": SessionLocalDWH,
}


def get_engine(db_name: str):
    engine = ENGINES.get(db_name)
    if engine is None:
        raise ValueError(f"Unknown database name: {db_name}")
    return engine


def get_session(db_name: str):
    session_factory = SESSIONS.get(db_name)
    if session_factory is None:
        raise ValueError(f"Unknown database name: {db_name}")
    return session_factory()