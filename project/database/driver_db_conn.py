import os
import sqlite3

DB_CONN_STR = "DB_CONN_STR"


def get_session():
    conn = sqlite3.connect(os.getenv(DB_CONN_STR))
    return conn
