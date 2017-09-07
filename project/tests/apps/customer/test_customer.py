# Import the Sanic app, usually created with Sanic(__name__)
import json
import unittest
from unittest.mock import Mock
from sanic import Blueprint, Sanic
from sqlalchemy.exc import IntegrityError

from apps.common.controller.request_manager import RequestManager
from apps.customer.controller.customer_controller import Customer, CustomerInstance
from apps.customer.model.tables import CustomerModel
from utils.auth import validate_auth_token

REQUEST_BODY = {
    "cnpjCpf": "00000000000",
    "customerName": "Testing Man",
    "address": "AV GEN JUSTO",
    "addressNumber": "375",
    "additionalInformation": "9 ANDAR",
    "district": "RIO DE JANEIRO",
    "city": "RIO DE JANEIRO",
    "state": "RJ",
    "zipCode": "20021130",
    "emailAddress": "tester@thatapp.com.br",
    "contactName": "tester",
    "phoneNumber": "000000000000",
    "emailInvoice": "tester@thatapp.com.br",
    "cityIbgeCode": "",
    "country": "BR"
}


class MockRequestManager(object):
    @staticmethod
    def get_org_name_from_request(a, b):
        return "OFFLINE"

    @staticmethod
    def get_page_from_request(a):
        return 0

    @staticmethod
    def get_data_paginated(a, b, c, d, *args):
        data = CustomerModel(CNPJ_CPF="0",
                             ORG_NAME="company_name",
                             ORG_ID="company_id",
                             CUSTOMER_NAME="customerName",
                             ADDRESS="address",
                             ADDRESS_NUMBER="addressNumber",
                             ADDITIONAL_INFORMATION="additionalInformation",
                             DISTRICT="district",
                             CITY="city",
                             STATE="state",
                             ZIP_CODE="zipCode",
                             EMAIL_ADDRESS="emailAddress",
                             CONTACT_NAME="contactName",
                             PHONE_NUMBER="phoneNumber",
                             STATUS="SUCCESS",
                             MESSAGE="CREATE",
                             EMAIL_INVOICE="emailInvoice",
                             CITY_IBGE_CODE="cityIbgeCode",
                             STATUS_EMAIL_INVOICE="SUCCESS",
                             COUNTRY="country")
        return [data]


class TestCustomerController(unittest.TestCase):
    def get_app(self, session_maker=Mock()):
        blueprint = Blueprint('app')
        blueprint.add_route(Customer.as_view(session_maker), '/customer')
        blueprint.add_route(CustomerInstance.as_view(session_maker), '/customer/<customer_id>')

        @blueprint.middleware('request')
        def mid(request):
            return validate_auth_token(request)

        app = Sanic()
        app.blueprint(blueprint)
        return app

    def test_post_missing_request_body(self):
        app = self.get_app()
        request, response = app.test_client.post('/customer', data=json.dumps({"eventType": 1}))
        assert response.status == 401

    def test_post_request_ok(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        request, response = app.test_client.post('/customer',
                                                 headers={"Authorization": "1",
                                                          "Content-Type": "application/json"},
                                                 data=json.dumps(REQUEST_BODY))
        assert response.status == 200

    def test_post_request_integrity_error(self):
        sessionmaker = Mock()
        sessionmaker.return_value.commit.side_effect = IntegrityError("Broken", {}, None)
        app = self.get_app(session_maker=sessionmaker)
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request

        request, response = app.test_client.post('/customer',
                                                 headers={"Authorization": "1",
                                                          "Content-Type": "application/json"},
                                                 data=json.dumps(REQUEST_BODY))
        assert response.status == 409

    def test_post_request_Exception(self):
        sessionmaker = Mock()
        sessionmaker.return_value.commit.side_effect = Exception("Broken", {}, None)
        app = self.get_app(session_maker=sessionmaker)
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request

        request, response = app.test_client.post('/customer',
                                                 headers={"Authorization": "1",
                                                          "Content-Type": "application/json"},
                                                 data=json.dumps(REQUEST_BODY))
        assert response.status == 400

    def test_get_request_failed(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        request, response = app.test_client.get('/customer', headers={"Authorization": "1",
                                                                      "Content-Type": "application/json"})
        assert response.status == 500

    def test_get_request_ok(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        RequestManager.get_data_paginated = MockRequestManager.get_data_paginated
        request, response = app.test_client.get('/customer', headers={"Authorization": "1",
                                                                      "Content-Type": "application/json"})
        assert response.status == 200

    def test_get_instance_request_ok(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        RequestManager.get_entry_from_request_with_id = MockRequestManager.get_data_paginated
        request, response = app.test_client.get('/customer/1', headers={"Authorization": "1",
                                                                      "Content-Type": "application/json"})
        assert response.status == 200

    def test_get_instance_request_failed(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        request, response = app.test_client.get('/customer/1', headers={"Authorization": "1",
                                                                      "Content-Type": "application/json"})
        assert response.status == 500

if __name__ == '__main__':
    unittest.main()
