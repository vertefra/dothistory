import logging
import sys
# import asyncio

from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

from project.app.config import get_settings, Settings

log = logging.getLogger(__name__)


class Db():
    def __init__(
            self,
            app: FastAPI = None,
            testing: bool = False,
            tables: list = []
    ):

        self.app: FastAPI = app
        self.settings: Settings = None
        self.testing: bool = testing
        self.db_name: str = None
        self.db_url: str = None
        self.engine: Engine = None
        self.localSession: Session = None
        self.tables = tables

        # initializing database engine

        self.set_settings()
        self.init_engine()
        self.set_base()
        self.set_local_session()

    def set_settings(self):
        ''' Loads the current env settings '''

        self.settings = get_settings()

    def set_tables(self, db_tables: list):
        self.tables = db_tables

    def bind_fastAPI(self, app: FastAPI):
        self.app = app

    def init_engine(self) -> Engine:
        ''' Initialize the engine. require the connection string for
        postgres database can be found in config.Settings class returned by
        get_settings. If engine.connect() returns an error meaning there is`
        no databse, it will create a new database. testing default False '''

        self.db_name = self.settings.dev_db if (
            self.testing is False) else self.settings.dev_db

        self.db_url = self.settings.database_url

        self.connection_url = self.db_url + self.db_name

        try:
            engine = create_engine(self.connection_url)
            engine.connect()

            self.engine = engine

            return engine

        except OperationalError as err:

            print("database does not exist")
            print(err)
            print("-----------------------")
            print("creating database")

            engine = create_engine(self.db_url)
            conn = engine.connect()
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(f"CREATE DATABASE {self.db_name}")

            self.init_engine()

    def set_local_session(self) -> Session:
        if self.engine is None:
            raise EnvironmentError("Engine value is None. ")
            sys.exit(1)
        else:
            session = sessionmaker(
                bind=self.engine, autoflush=False, autocommit=False)
            self.localSession = session
            return session

    def set_base(self):
        self.base = declarative_base(bind=self.engine)
        return self.base

    def create_tables(self):
        if len(self.tables) != 0:
            db_tables = [table.__table__ for table in self.tables]
            self.base.metadata.create_all(
                bind=self.engine,
                tables=db_tables,
                checkfirst=True
            )

        else:
            raise ValueError("Can't create tables. tables attribute is empty")

    def get_db(self) -> Session:

        db = self.localSession()
        try:
            yield db
        finally:
            db.close()


db_engine = Db()
