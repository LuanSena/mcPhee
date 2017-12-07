from sanic import Sanic
from sanic.config import Config
from sanic_cors import CORS
# from sanic.config import Config
from apps.classes.urls import ClassesBP
from apps.diary.urls import DiaryBP
from apps.person.urls import PersonBP
from apps.school.urls import SchoolBP
from apps.student.urls import StudentBP


def get_app(session):
    Config.REQUEST_TIMEOUT = 9999999999
    app = Sanic()

    person = PersonBP(session)
    school = SchoolBP(session)
    student = StudentBP(session)
    diary = DiaryBP(session)
    classes = ClassesBP(session)

    app.blueprint(person.blueprint)
    app.blueprint(school.blueprint)
    app.blueprint(student.blueprint)
    app.blueprint(diary.blueprint)
    app.blueprint(classes.blueprint)

    CORS(app)
    return app
