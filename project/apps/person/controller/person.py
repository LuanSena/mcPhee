from sanic.response import json, text
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from database import db_request_manager


class Person(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request):
        return text("ok")

    async def post(self, request):
        try:
            request = request.json

            person_id = db_request_manager.insert_person(self.db_conn, request)
            response = {"success": True,
                        "person": "v1/person/" + str(person_id)}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request):
        persons = db_request_manager.get_persons(self.db_conn)
        return json(persons, 200)


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
