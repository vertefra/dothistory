import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def init_db(db_url: str) -> Engine:
    engine = create_engine(db_url)
    return engine


def create_db_if_not_exists(engine: Engine, db_name: str):
    # Creating connection instance out of the Engine class
    # Will use SQL to check if database exists and create
    # it in case it doesnt based on the current configuration
    conn = engine.connect()

    try:
        conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print("Database created")
    except Exception as err:
        print("Failed creating database")
        print("Error: ", err)
        os.Exit(1)
