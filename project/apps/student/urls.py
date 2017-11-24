from sanic import Blueprint

from apps.student.controller.student import Student, StudentInstance, StudentSchool, StudentProf


class StudentBP:
    def __init__(self, db_conn):
        blueprint = Blueprint('student')

        blueprint.add_route(Student.as_view(db_conn), '/v1/student')
        blueprint.add_route(StudentInstance.as_view(db_conn), '/v1/student/<student_id>')
        blueprint.add_route(StudentSchool.as_view(db_conn), '/v1/student/school/<school_id>')
        blueprint.add_route(StudentProf.as_view(db_conn), '/v1/student/prof/<person_id>')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
