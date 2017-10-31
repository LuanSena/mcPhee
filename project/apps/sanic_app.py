from sanic import Sanic
from sanic_cors import CORS

from apps.person.urls import PersonBP


def get_app(session):
    app = Sanic()

    person = PersonBP(session)
    app.blueprint(person.blueprint)
    CORS(app)
    return app
