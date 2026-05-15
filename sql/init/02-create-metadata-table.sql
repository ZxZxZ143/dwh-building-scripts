CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS metadata.etl_watermarks (
    source_name text PRIMARY KEY,
    last_loaded_at timestamp NOT NULL
);