import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONN_STR = "DB_CONN_STR"


def get_session():
    # sqlite_conn = "sqlite:////absolute/path/to/foo.db"
    sqlite_conn = 'sqlite:////home/luan/Downloads/SQLiteStudio/dbs/mcphee'
    sql_alchemy_conn = os.getenv(DB_CONN_STR, False)
    if sql_alchemy_conn is False:
        sql_alchemy_conn = sqlite_conn
    engine = create_engine(sql_alchemy_conn, echo=True)
    session_maker = sessionmaker(bind=engine)
    return session_maker
