from sanic.response import json, text
from sanic.views import HTTPMethodView

from database import db_request_manager


class PersonLogin(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request):
        return text("ok")

    async def post(self, request):
        try:
            user = request.headers['user']
            password = request.headers['password']
            person = db_request_manager.get_person_by_login(db_conn=self.db_conn, user=user, password=password)
            if person:
                return json(person, 200)
            return json({"success": False,
                         "message": "No result were found"}, 401)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
