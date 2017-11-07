from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from project.database import db_request_manager


class PersonClasses(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, person_id):
        try:
            classes = db_request_manager.get_person_classes_by_id(self.db_conn, person_id)
            return json(classes, 200)

        except NoResultFound as e:
            print(str(e))
            return json({"success": False,
                         "message": "No result were found"}, 404)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
