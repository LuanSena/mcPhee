from sanic.response import json
from sanic.views import HTTPMethodView

from apps.common.controller.request_manager import RequestManager
from apps.invoice.model.tables import InvoiceModel
from apps.professional.model.professional_mapping import ProfessionalModel


class Professional(HTTPMethodView):
    def __init__(self, session_maker):
        self.professionalID = None
        self.session_maker = session_maker
        self.page_size = 500
        self.page = None

    async def post(self, request):
        try:
            session = self.session_maker()
            request = request.json
            professional = ProfessionalModel()
            professional = professional.set_model(name=request["cnpjCpf"],
                                                  address_number=request["amount"],
                                                  document=request["origSysRef"],
                                                  email=request["email"],
                                                  occupation=request["occupation"],
                                                  rotation=request["rotation"],
                                                  cep=request["cep"]
                                                  )
            session.add(professional)
            session.commit()

            response = {"success": True,
                        "professional": "/professional/" + str(professional.professionalID)}

            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def get(self, request):
        try:
            company = request["company"]
            self.page = RequestManager.get_page_from_request(request)
            session = self.session_maker()
            rows = RequestManager.get_data_paginated(InvoiceModel, session, company, self.page, self.page_size)
            response = self._build_response(rows)
            session.close()

            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    @staticmethod
    def _build_response(rows):
        response = [{"cnpjCpf": row.CNPJ_CPF,
                     "amount": row.AMOUNT,
                     "operation": row.OPERATION,
                     "transactionDate": row.TRANSACTION_DATE,
                     "city": row.CITY,
                     "state": row.STATE,
                     "comments": row.COMMENTS} for row in rows]
        return response


class InvoiceInstance(HTTPMethodView):
    def __init__(self, session_maker):
        self.session_maker = session_maker
        self.company_id = None

    async def get(self, request, invoice_id):
        try:
            session = self.session_maker()
            self.company_id = RequestManager.get_org_name_from_request(request, session)
            invoice = RequestManager.get_entry_from_request_with_id(InvoiceModel, self.company_id, invoice_id, session)
            response = self._build_response(invoice)
            session.close()
            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    @staticmethod
    def _build_response(rows):
        response = [{"cnpjCpf": row.CNPJ_CPF,
                     "amount": row.AMOUNT,
                     "operation": row.OPERATION,
                     "transactionDate": row.TRANSACTION_DATE,
                     "city": row.CITY,
                     "state": row.STATE,
                     "comments": row.COMMENTS} for row in rows]
        return response
