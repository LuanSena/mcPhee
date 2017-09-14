from sanic.response import json
from sanic.views import HTTPMethodView

from apps.professional.model.professional import ProfessionalModel


class Professional(HTTPMethodView):
    def __init__(self, session_maker):
        self.session_maker = session_maker
        self.page_size = 500
        self.page = None

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

            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
        finally:
            session.commit()

    async def get(self, request, prof_id):
        try:
            session = self.session_maker()

            professional = ProfessionalModel()
            professional.get_by_professional_id(session, prof_id)

            session.close()
            return json(professional, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
