from sanic.response import json
from sanic.views import HTTPMethodView

from apps.common.controller.request_manager import RequestManager
from apps.invoice.model.tables import InvoiceModel


class Invoice(HTTPMethodView):
    def __init__(self, session_maker):
        self.company_id = None
        self.session_maker = session_maker
        self.page_size = 500
        self.page = None
        self.company_name = None

    async def post(self, request):
        try:
            session = self.session_maker()
            self.company_id = request["company"]
            self.company_name = RequestManager.get_org_name_from_request(request, session)
            request = request.json

            invoice = InvoiceModel(ORG_ID=self.company_id,
                                   ORG_CODE=self.company_name,
                                   CNPJ_CPF=request["cnpjCpf"],
                                   AMOUNT=request["amount"],
                                   ORIG_SYS_REF=request["origSysRef"],
                                   CURRENCY_CODE="BRL",
                                   OPERATION=1,
                                   TRANSACTION_DATE=request["transactionDate"],
                                   CITY=request["city"],
                                   STATE=request["state"],
                                   COMMENTS=request["comments"],
                                   )
            session.add(invoice)
            session.commit()

            response = {"success": True,
                        "invoice": "/invoice/" + str(invoice.ID)}

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
