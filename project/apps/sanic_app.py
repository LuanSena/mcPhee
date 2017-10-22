from sanic import Sanic

from apps.person.urls import PersonBP


def get_app(session):
    app = Sanic()

    person = PersonBP(session)
    app.blueprint(person.blueprint)
    return app
