from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from project.database import db_request_manager


class Prof(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, school_id):
        try:
            profs = db_request_manager.get_profs_by_school(self.db_conn, school_id)
            return json(profs, 200)
        except NoResultFound as e:
            print(str(e))
            return json({"success": False,
                         "message": "No result were found"}, 404)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
