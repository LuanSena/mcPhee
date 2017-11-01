from sanic import Sanic
from sanic_cors import CORS

from apps.person.urls import PersonBP
from apps.school.urls import SchoolBP


def get_app(session):
    app = Sanic()

    person = PersonBP(session)
    school = SchoolBP(session)
    app.blueprint(person.blueprint)
    app.blueprint(school.blueprint)

    CORS(app)
    return app
