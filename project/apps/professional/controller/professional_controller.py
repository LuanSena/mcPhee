from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from apps.common.controller.request_manager import RequestManager
from apps.professional.model.professional import ProfessionalModel


class Professional(HTTPMethodView):
    def __init__(self, session_maker):
        self.session_maker = session_maker
        self.page_size = 100
        self.page = None

    async def post(self, request):
        session = self.session_maker()
        try:
            request = request.json
            professional = ProfessionalModel(name=request["name"],
                                             address_number=request["addressNumber"],
                                             document=request["document"],
                                             occupation=request["occupation"],
                                             cep=request["cep"]
                                             )
            professional.add_new(session)


            response = {"success": True,
                        "professional": "/professional/" + str(professional.professional_id)}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
        finally:
            session.commit()

    async def get(self, request):
        session = self.session_maker()
        self.page = RequestManager.get_page_from_request(request)
        result = ProfessionalModel.get_paginated(session=session, page=self.page, page_size=self.page_size)
        response = self._build_professional_response(result)
        return json(response, 200)

    def _build_professional_response(self, objects):
        response = list()
        for entry in objects:
            response.append({"name": entry.name[0],
                             "addressNumber": entry.address_number[0],
                             "document": entry.document[0],
                             "occupation": entry.occupation[0],
                             # "rotation": entry.rotation,
                             # "cep": entry.cep,
                             "userId": entry.user_id[0],
                             "professionalId": entry.professional_id[0]})
        return response

class ProfessionalInstance(HTTPMethodView):
    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def get(self, request, prof_id):
        try:
            session = self.session_maker()

            professional = ProfessionalModel()
            professional.get_by_professional_id(session, prof_id)

            session.close()
            return json(professional, 200)

        except NoResultFound as e:
            print(str(e))
            return json({"success": False,
                         "message": "No result were found"}, 404)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
