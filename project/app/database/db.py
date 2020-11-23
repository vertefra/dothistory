import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

from project.app.config import get_settings

log = logging.getLogger(__name__)


def init_db(database_url: str, db_name: str = "dev_db") -> Engine:
    ''' Initialize the engine database. require the connection string for
    postgres database can be found in config.Settings class returned by
    get_settings. If engine.connect() returns an error meaning there is`
    no databse, it will create a new database '''

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
        conn.execute(f"CREATE DATABASE {db_name}")
        print(" - database created - ")
        init_db(database_url)
    return engine


def get_db(session: Session) -> Session:
    ''' Returns a db instance '''

    db = session()
    try:
        return db
    finally:
        db.close()


def create_tables(db_tables: list):
    db_tables = [table.__table__ for table in db_tables]
    Base.metadata.create_all(bind=engine, tables=db_tables, checkfirst=True)


engine = init_db(get_settings().database_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base(bind=engine)
