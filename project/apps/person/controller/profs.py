from sanic.response import json, text
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from database import db_request_manager


class Prof(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request):
        return text("ok")

    async def post(self, request):
        try:
            request = request.json
            school_id = request['schoolId']
            person_doc = request['personDocument']
            person_id = db_request_manager.get_person_by_document(self.db_conn, person_doc)
            db_request_manager.insert_prof(self.db_conn, school_id, person_id)
            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request, school_id=None):
        classes = db_request_manager.get_classes_by_school(self.db_conn, school_id)
        return json(classes, 200)

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
