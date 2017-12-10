from sanic import Blueprint

from apps.classes.controller.classes import Classes, ClassProf, ClassStudent, ClassDetail, ClassDetailStudent


class ClassesBP:
    def __init__(self, db_conn):
        blueprint = Blueprint('classes')

        blueprint.add_route(Classes.as_view(db_conn), '/v1/class/<school_id>')
        blueprint.add_route(Classes.as_view(db_conn), '/v1/class')
        blueprint.add_route(ClassProf.as_view(db_conn), '/v1/class/prof')
        blueprint.add_route(ClassStudent.as_view(db_conn), '/v1/class/student')
        blueprint.add_route(ClassDetail.as_view(db_conn), '/v1/class/details/<class_id>')
        blueprint.add_route(ClassDetail.as_view(db_conn), '/v1/class/<class_id>/prof/<prof_id>')
        blueprint.add_route(ClassDetailStudent.as_view(db_conn), '/v1/class/<class_id>/student/<student_id>')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
