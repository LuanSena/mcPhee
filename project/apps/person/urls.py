from sanic import Blueprint

from project.apps.person.controller.person import Person, PersonInstance


class ProfessionalBP:
    def __init__(self, db_conn):
        blueprint = Blueprint('person')

        blueprint.add_route(Person.as_view(db_conn), '/person')
        blueprint.add_route(PersonInstance.as_view(db_conn), '/person/<prof_id>')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
