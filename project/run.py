import sys

from apps import sanic_app

if __name__ == "__main__":
    try:
        app = sanic_app.get_app()
        app.run(host="0.0.0.0", port=8888, debug=False)
    except Exception as error:
        sys.stderr.write("Error while starting application: %s" % error)
        raise error

