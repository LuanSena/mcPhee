from sanic import Blueprint

from apps.person.controller.manager import Manager
from apps.person.controller.person_classes import PersonClasses
from apps.person.controller.person_login import PersonLogin
from apps.person.controller.profs import Prof
from project.apps.person.controller.person import Person, PersonInstance


class PersonBP:
    def __init__(self, db_conn):
        blueprint = Blueprint('person')

        blueprint.add_route(Person.as_view(db_conn), '/v1/person')
        blueprint.add_route(PersonInstance.as_view(db_conn), '/v1/person/<prof_id>')
        blueprint.add_route(PersonClasses.as_view(db_conn), '/v1/person/<person_id>/classes')

        blueprint.add_route(Manager.as_view(db_conn), '/v1/person/managers')
        blueprint.add_route(Prof.as_view(db_conn), '/v1/person/prof/<school_id>')

        blueprint.add_route(PersonLogin.as_view(db_conn), '/v1/auth')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
