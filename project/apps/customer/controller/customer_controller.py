from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy.exc import IntegrityError

from apps.common.controller.request_manager import RequestManager
from apps.customer.model.tables import CustomerModel


class Customer(HTTPMethodView):
    def __init__(self, session_maker):
        self.session_maker = session_maker
        self.page_size = 500
        self.page = None
        self.company_id = None
        self.company_name = None

    async def get(self, request):
        try:
            self.company_id = request["company"]
            self.page = RequestManager.get_page_from_request(request)
            session = self.session_maker()
            rows = RequestManager.get_data_paginated(CustomerModel, session, self.company_id, self.page, self.page_size)
            response = self._build_response(rows)
            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    async def post(self, request):
        try:
            session = self.session_maker()
            body = request.json
            self.company_name = RequestManager.get_org_name_from_request(request, session)
            self.company_id = request["company"]
            customer = CustomerModel(CNPJ_CPF=body["cnpjCpf"],
                                     ORG_NAME=self.company_name,
                                     ORG_ID=self.company_id,
                                     CUSTOMER_NAME=body["customerName"],
                                     ADDRESS=body["address"],
                                     ADDRESS_NUMBER=body["addressNumber"],
                                     ADDITIONAL_INFORMATION=body["additionalInformation"],
                                     DISTRICT=body["district"],
                                     CITY=body["city"],
                                     STATE=body["state"],
                                     ZIP_CODE=body["zipCode"],
                                     EMAIL_ADDRESS=body["emailAddress"],
                                     CONTACT_NAME=body["contactName"],
                                     PHONE_NUMBER=body["phoneNumber"],
                                     STATUS="SUCCESS",
                                     MESSAGE="CREATE",
                                     EMAIL_INVOICE=body["emailInvoice"],
                                     CITY_IBGE_CODE=body["cityIbgeCode"],
                                     STATUS_EMAIL_INVOICE="SUCCESS",
                                     COUNTRY=body["country"])
            session.add(customer)
            session.commit()
            return json({"success": True,
                         "customer": "/customer/" + str(customer.CNPJ_CPF)}, 200)
        except IntegrityError as e:
            print(str(e))
            return json({"success": False,
                         "message": "Resource already exists"}, 409)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "error": "unexpected error has occurred"}, 400)

    @staticmethod
    def _build_response(rows):
        response = [{"cnpjCpf": row.CNPJ_CPF,
                     "orgName": row.ORG_NAME,
                     "customerName": row.CUSTOMER_NAME.strip(),
                     "address": row.ADDRESS,
                     "addressNumber": row.ADDRESS_NUMBER,
                     "additionalInformation": row.ADDITIONAL_INFORMATION,
                     "district": row.DISTRICT,
                     "city": row.CITY,
                     "state": row.STATE,
                     "zipCode": row.ZIP_CODE,
                     "emailAddress": row.EMAIL_ADDRESS,
                     "contactName": row.CONTACT_NAME,
                     "phoneNumber": row.PHONE_NUMBER,
                     "status": row.STATUS,
                     "message": row.MESSAGE,
                     "emailInvoice": row.EMAIL_INVOICE,
                     "cityIbgeCode": row.CITY_IBGE_CODE,
                     "statusEmailInvoice": row.STATUS_EMAIL_INVOICE,
                     "country": row.COUNTRY} for row in rows]
        return response


class CustomerInstance(HTTPMethodView):
    def __init__(self, session_maker):
        self.session_maker = session_maker
        self.company_id = None

    def get(self, request, customer_id):
        try:
            session = self.session_maker()
            self.company_id = RequestManager.get_org_name_from_request(request, session)
            customer = RequestManager.get_entry_from_request_with_id(CustomerModel, self.company_id, customer_id, session)
            response = self._build_response(customer)
            return json(response, 200)
        except Exception as e:
            print(str(e))
            return json({"success": False,
                         "message": "unexpected error has occurred"}, 500)

    @staticmethod
    def _build_response(rows):
        response = [{"cnpjCpf": row.CNPJ_CPF,
                     "orgName": row.ORG_NAME,
                     "customerName": row.CUSTOMER_NAME.strip(),
                     "address": row.ADDRESS,
                     "addressNumber": row.ADDRESS_NUMBER,
                     "additionalInformation": row.ADDITIONAL_INFORMATION,
                     "district": row.DISTRICT,
                     "city": row.CITY,
                     "state": row.STATE,
                     "zipCode": row.ZIP_CODE,
                     "emailAddress": row.EMAIL_ADDRESS,
                     "contactName": row.CONTACT_NAME,
                     "phoneNumber": row.PHONE_NUMBER,
                     "status": row.STATUS,
                     "message": row.MESSAGE,
                     "emailInvoice": row.EMAIL_INVOICE,
                     "cityIbgeCode": row.CITY_IBGE_CODE,
                     "statusEmailInvoice": row.STATUS_EMAIL_INVOICE,
                     "country": row.COUNTRY} for row in rows]
        return response
