from sanic.response import json
from sanic.views import HTTPMethodView

from project.database import db_request_manager


class DiaryPerClass(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def post(self, request, class_id):
        try:
            request = request.json
            students = db_request_manager.get_student_by_class_id(self.db_conn, class_id)

            for student in students:
                db_request_manager.insert_diary(self.db_conn, student, request["diaryText"])

            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)


class DiaryPerStudent(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def post(self, request, student_id):
        try:
            request = request.json
            db_request_manager.insert_diary(self.db_conn, student_id, request["diaryText"])

            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
