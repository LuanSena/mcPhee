from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from project.database import db_request_manager


class Student(HTTPMethodView):
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
        schools = db_request_manager.get_students_by_schoool(self.db_conn, '%')
        return json(schools, 200)


class StudentSchool(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, school_id):
        schools = db_request_manager.get_students_by_schoool(self.db_conn, school_id)
        return json(schools, 200)


class StudentInstance(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, student_id):
        try:
            student = db_request_manager.get_student_by_id(self.db_conn, student_id)
            student["diarys"] = db_request_manager.get_student_diary_by_id(self.db_conn, student_id, 10)
            return json(student, 200)

        except NoResultFound as e:
            print(str(e))
            return json({"success": False,
                         "message": "No result were found"}, 404)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
