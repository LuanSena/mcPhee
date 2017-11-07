from sanic import Blueprint

from apps.diary.controller.diary import DiaryPerClass, DiaryPerStudent


class DiaryBP:
    def __init__(self, db_conn):
        blueprint = Blueprint('diary')

        blueprint.add_route(DiaryPerClass.as_view(db_conn), '/v1/diary/class/<class_id>')
        blueprint.add_route(DiaryPerStudent.as_view(db_conn), '/v1/diary/student/<student_id>')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
