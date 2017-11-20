from sanic import Sanic
from sanic_cors import CORS
# from sanic.config import Config

from apps.diary.urls import DiaryBP
from apps.person.urls import PersonBP
from apps.school.urls import SchoolBP
from apps.student.urls import StudentBP


def get_app(session):
    # Config.REQUEST_TIMEOUT = 3
    app = Sanic()

    person = PersonBP(session)
    school = SchoolBP(session)
    student = StudentBP(session)
    diary = DiaryBP(session)

    app.blueprint(person.blueprint)
    app.blueprint(school.blueprint)
    app.blueprint(student.blueprint)
    app.blueprint(diary.blueprint)

    CORS(app)
    return app
