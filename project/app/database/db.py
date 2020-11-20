from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def init_db(database_url: str) -> Engine:
    engine = create_engine(database_url)
    try:
        engine.connect()
    except OperationalError as err:
        print("database does not exist")
        print(err)
        print("-----------------------")
        print("creating database")
        engine = create_engine("postgres://postgres:postgres@postgres-db:5432")
        conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
        conn.execute("CREATE DATABASE dev_db")
        print(" - database created - ")
        init_db(database_url)
    return engine


def create_tables(engine: Engine) -> bool:
    try:
        print(" ------------------------ ")
        print(" creating tables          ")
        Base.metadata.create_all(engine)
        return True
    except Exception as err:
        print("Error in create_tables")
        print("Error: ", err)
        return False
