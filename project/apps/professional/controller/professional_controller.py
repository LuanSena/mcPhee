from sanic.response import json
from sanic.views import HTTPMethodView

from apps.professional.model.professional import ProfessionalModel


class Professional(HTTPMethodView):
    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def post(self, request):
        session = self.session_maker()
        try:
            request = request.json
            professional = ProfessionalModel(name=request["name"],
                                             address_number=request["addressNumber"],
                                             document=request["document"],
                                             occupation=request["occupation"],
                                             rotation=request["rotation"],
                                             cep=request["cep"]
                                             )
            professional.add_new(session)


            response = {"success": True,
                        "professional": "/professional/" + str(professional.professional_id)}
            print(response)

            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
        finally:
            session.commit()
