from sanic import Blueprint

from apps.person.controller.person_classes import PersonClasses
from apps.person.controller.person_login import PersonLogin
from project.apps.person.controller.person import Person, PersonInstance


class PersonBP:
    def __init__(self, db_conn):
        blueprint = Blueprint('person')

        blueprint.add_route(Person.as_view(db_conn), '/v1/person')
        blueprint.add_route(PersonInstance.as_view(db_conn), '/v1/person/<prof_id>')
        blueprint.add_route(PersonClasses.as_view(db_conn), '/v1/person/<person_id>/diary')

        blueprint.add_route(PersonLogin.as_view(db_conn), '/v1/auth')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
