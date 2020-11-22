from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


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


def create_tables(engine: Engine) -> bool:
    ''' Creates database tables. Require a SQLAlchemy database engine
    connected to a posgres database'''
    try:
        print(" ------------------------ ")
        print(" creating tables          ")
        Base.metadata.create_all(engine)
        return True
    except Exception as err:
        print("Error in create_tables")
        print("Error: ", err)
        return False


def get_db(engine: Engine) -> Session:
    ''' Returns a Session '''
    db = sessionmaker(bind=engine)
    try:
        yield db
    finally:
        db.close()
