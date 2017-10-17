from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy.orm.exc import NoResultFound

from project.database import db_request_manager


class Person(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def post(self, request):
        try:
            request = request.json
            name = request["name"],
            age = request["age"],
            document = request["document"],
            atribute = request["atribute"],
            address_name = request["addressName"],
            addres_number = request["addresNumber"],
            address_complement = request["addressComplement"],
            email = request["email"],
            password = request["password"],
            contact = request["Contact"]

            person_id = db_request_manager.insert_person(self.db_conn(), name, age, document, atribute, address_name,
                                                         addres_number, address_complement, email, password, contact)
            response = {"success": True,
                        "person": "v1/person/" + str(person_id)}

            return json(response, 202)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request):
        # session = self.db_conn()
        # self.page = RequestManager.get_page_from_request(request)
        # result = ProfessionalModel.get_paginated(session=session, page=self.page, page_size=self.page_size)
        # response = self._build_professional_response(result)
        # return json(response, 200)
        pass

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


class PersonInstance(HTTPMethodView):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def get(self, request, prof_id):
        try:
            person = db_request_manager.get_person_by_id(self.db_conn, prof_id)
            return json(person, 200)

        except NoResultFound as e:
            print(str(e))
            return json({"success": False,
                         "message": "No result were found"}, 404)

        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)
