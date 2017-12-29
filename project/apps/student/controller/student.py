from sanic.response import json, text
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from database import db_request_manager


class Student(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request):
        return text("ok")

    async def post(self, request):
        try:
            request = request.json
            name = request["studentName"]
            grade = request["studentGrade"]
            born_date = request["studentBorn_date"]
            nacionality = request["studentNacionality"]
            eating_obs = request["studentEating_obs"]
            obs = request["studentObs"]
            school_id = request["schoolId"]

            db_request_manager.insert_student(self.db_conn,
                                              name,
                                              grade,
                                              born_date,
                                              nacionality,
                                              eating_obs,
                                              obs,
                                              school_id)
            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request):
        students = db_request_manager.get_students_by_schoool(self.db_conn, '%')
        return json(students, 200)


class StudentSchool(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, school_id):
        students = db_request_manager.get_students_by_schoool_simplifed(self.db_conn, school_id)
        return json(students, 200)


class StudentProf(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, person_id):
        schools = db_request_manager.get_students_by_professional(self.db_conn, person_id)
        return json(schools, 200)


class StudentInstance(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, student_id):
        try:
            student = db_request_manager.get_student_by_id(self.db_conn, student_id)
            student["schoolName"] = None
            student["className"] = None
            if student["class_id"]:
                student["className"], school_id = db_request_manager.get_class_name_by_id(self.db_conn, student["class_id"])
                school = db_request_manager.get_school_by_id(self.db_conn, school_id)
                student["schoolName"] = school["fantasyName"]
            student["diarys"] = db_request_manager.get_student_diary_by_id(self.db_conn, student_id, 10)
            student["owners"] = db_request_manager.get_student_owners_by_student_id(self.db_conn, student_id)
            return json(student, 200)

        except NoResultFound as e:
            print(str(e))
            return json({"success": False,
                         "message": "No result were found"}, 404)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)


class StudentOwner(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request, student_id):
        return text("ok")

    async def post(self, request, student_id):
        try:
            request = request.json
            owner = request["ownerDocument"]
            db_request_manager.insert_student_owner(self.db_conn, owner, student_id)
            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request):
        students = db_request_manager.get_students_by_schoool(self.db_conn, '%')
        return json(students, 200)
