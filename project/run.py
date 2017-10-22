import sys

from apps import sanic_app
from database import driver_db_conn

if __name__ == "__main__":
    try:
        db_connection = driver_db_conn.get_session()
        app = sanic_app.get_app(db_connection)
        app.run(host="0.0.0.0", port=8888, debug=False, log_config=None)
    except Exception as error:
        sys.stderr.write("Error while starting application: %s" % error)
        raise error

