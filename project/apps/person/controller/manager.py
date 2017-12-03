from sanic.response import json, text
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from project.database import db_request_manager


class Manager(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request):
        return text("ok")

    async def post(self, request):
        try:
            request = request.json
            person_id = db_request_manager.get_person_by_document(self.db_conn, request['document'])
            school_id = request['schoolId']
            db_request_manager.insert_manager(self.db_conn, person_id, school_id)
            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request):
        managers = db_request_manager.get_managers(self.db_conn)
        return json(managers, 200)


class PersonInstance(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, prof_id):
        try:
            person = db_request_manager.get_person_by_id(self.db_conn, prof_id)
            return json(person, 200)

        except NoResultFound as e:
            print(str(e))
            return json({"success": False,
                         "message": "No result were found"}, 404)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
