import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONN_STR = "DB_CONN_STR"


def get_session():
    sql_alchemy_conn = os.getenv(DB_CONN_STR)

    engine = create_engine(sql_alchemy_conn, echo=True)
    session_maker = sessionmaker(bind=engine)
    return session_maker
