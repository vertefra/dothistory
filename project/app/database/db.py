import logging
# import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

from project.app.config import get_settings

log = logging.getLogger(__name__)


def init_db(testing: bool = False) -> Engine:
    ''' Initialize the engine database. require the connection string for
        postgres database can be found in config.Settings class returned by
        get_settings. If engine.connect() returns an error meaning there is`
        no databse, it will create a new database. testing default False '''

    settings = get_settings()

    db_name = "dev_db" if testing is False else "test_db"

    db_url = settings.database_url + db_name

    try:

        engine = create_engine(db_url)
        engine.connect()

        return engine

    except OperationalError as err:

        print("database does not exist")
        print(err)
        print("-----------------------")
        print("creating database")

        engine = create_engine(settings.database_url)
        conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(f"CREATE DATABASE {db_name}")

        print(" - database created - ")
        init_db(db_url)


def get_db() -> Session:
    ''' Returns a db instance '''

    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def create_tables(db_tables: list, engine: Engine):
    '''Creates tables descripted in models and added to db_tables in main.py'''

    print(' - Creating Tables if not exists')

    db_tables = [table.__table__ for table in db_tables]
    Base.metadata.create_all(bind=engine, tables=db_tables, checkfirst=True)


engine = init_db(get_settings().database_url)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base(bind=engine)
