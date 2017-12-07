from sanic import Blueprint

from apps.classes.controller.classes import Classes, ClassProf, ClassStudent


class ClassesBP:
    def __init__(self, db_conn):
        blueprint = Blueprint('classes')

        blueprint.add_route(Classes.as_view(db_conn), '/v1/class/<school_id>')
        blueprint.add_route(Classes.as_view(db_conn), '/v1/class')
        blueprint.add_route(ClassProf.as_view(db_conn), '/v1/class/prof')
        blueprint.add_route(ClassStudent.as_view(db_conn), '/v1/class/student')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
