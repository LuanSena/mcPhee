from sanic.response import json, text
from sanic.views import HTTPMethodView

from project.database import db_request_manager


class Classes(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request):
        return text("ok")

    async def post(self, request):
        try:
            request = request.json
            school_id = request['schoolId']
            class_name = request['className']
            db_request_manager.insert_class(self.db_conn, school_id, class_name)
            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request, school_id=None):
        classes = db_request_manager.get_classes_by_school(self.db_conn, school_id)
        return json(classes, 200)


class ClassProf(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request):
        return text("ok")

    async def post(self, request):
        try:
            request = request.json
            class_id = request['classId']
            prof_id = request['personId']
            db_request_manager.insert_class_prof(self.db_conn, class_id, prof_id)
            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)


class ClassStudent(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request):
        return text("ok")

    async def post(self, request):
        try:
            request = request.json
            class_id = request['classId']
            student_id = request['studentId']
            db_request_manager.insert_class_student(self.db_conn, class_id, student_id)
            response = {"success": True}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request, school_id=None):
        classes = db_request_manager.get_classes_by_school(self.db_conn, school_id)
        return json(classes, 200)


class ClassDetail(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request, class_id, prof_id):
        return text("ok")

    async def delete(self, request, class_id, prof_id):
        try:
            db_request_manager.delete_prof_from_class(self.db_conn, class_id, prof_id)
            response = {"success": True}

            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request, class_id):
        classDetail = dict()
        students = db_request_manager.get_student_by_class_id(self.db_conn, class_id)

        classDetail["students"] = list()
        for student in students:
            classDetail["students"].append(db_request_manager.get_student_by_id(self.db_conn, student["student_id"]))

        classDetail["profs"] = list()
        persons = db_request_manager.get_person_by_class_id(self.db_conn, class_id)
        for person in persons:
            classDetail["profs"].append(db_request_manager.get_person_by_id(self.db_conn,person))

            # classes = db_request_manager.get_classes_by_school(self.db_conn, school_id)
        return json(classDetail, 200)

class ClassDetailStudent(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def options(self, request, class_id, student_id):
        return text("ok")

    async def delete(self, request, class_id, student_id):
        try:
            db_request_manager.delete_student_from_class(self.db_conn, class_id, student_id)
            response = {"success": True}

            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
