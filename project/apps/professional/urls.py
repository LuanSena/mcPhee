from sanic import Blueprint

from apps.professional.controller.professional_controller import Professional


class ProfessionalBP:
    def __init__(self, session_maker):
        blueprint = Blueprint('professional')

        blueprint.add_route(Professional.as_view(session_maker), '/professional')
        blueprint.add_route(Professional.as_view(session_maker), '/professional/<prof_id>')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
