from sanic import Blueprint

from apps.school.controller.school import School, SchoolInstance


class SchoolBP:
    def __init__(self, db_conn):
        blueprint = Blueprint('school')

        blueprint.add_route(School.as_view(db_conn), '/v1/school')
        blueprint.add_route(SchoolInstance.as_view(db_conn), '/v1/school/<school_id>')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
