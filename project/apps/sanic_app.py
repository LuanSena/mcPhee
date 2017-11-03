from sanic import Sanic
from sanic_cors import CORS

from apps.person.urls import PersonBP
from apps.school.urls import SchoolBP
from apps.student.urls import StudentBP


def get_app(session):
    app = Sanic()

    person = PersonBP(session)
    school = SchoolBP(session)
    student = StudentBP(session)
    app.blueprint(person.blueprint)
    app.blueprint(school.blueprint)
    app.blueprint(student.blueprint)

    CORS(app)
    return app
