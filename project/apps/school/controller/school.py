from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from project.database import db_request_manager


class School(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def post(self, request):
        try:
            request = request.json

            school_id = db_request_manager.insert_school(self.db_conn, request)
            response = {"success": True,
                        "person": "v1/school/" + str(school_id)}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request):
        schools = db_request_manager.get_schools(self.db_conn)
        return json(schools, 200)


class SchoolInstance(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, school_id):
        try:
            school = db_request_manager.get_school_by_id(self.db_conn, school_id)
            school["turns"] = db_request_manager.get_school_turns_by_id(self.db_conn, school_id)
            return json(school, 200)

        except NoResultFound as e:
            print(str(e))
            return json({"success": False,
                         "message": "No result were found"}, 404)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
