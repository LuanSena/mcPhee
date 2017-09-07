# Import the Sanic app, usually created with Sanic(__name__)
import json
import unittest
from unittest.mock import Mock
from sanic import Blueprint, Sanic
from sqlalchemy.exc import IntegrityError

from apps.common.controller.request_manager import RequestManager
from apps.customer.controller.customer_controller import Customer, CustomerInstance
from apps.customer.model.tables import CustomerModel
from apps.invoice.controller.invoice_controller import Invoice, InvoiceInstance
from apps.invoice.model.tables import InvoiceModel
from utils.auth import validate_auth_token

REQUEST_BODY = {
    "cnpjCpf": "00000000000",
    "amount": "123",
    "origSysRef": "1321",
    "transactionDate": "2016-01-01 00:00:00",
    "city": "RIO DE JANEIRO",
    "state": "RJ",
    "comments": "zipCode"
}

DEFAULT_HEADER = {"Authorization": "1",
                  "Content-Type": "application/json"}


class MockRequestManager(object):
    @staticmethod
    def get_org_name_from_request(a, b):
        return "OFFLINE"

    @staticmethod
    def get_page_from_request(a):
        return 0

    @staticmethod
    def get_data_paginated(a, b, c, d, *args):
        data = InvoiceModel(ORG_ID="0",
                            ORG_CODE="company_name",
                            CNPJ_CPF="company_id",
                            AMOUNT="customerName",
                            ORIG_SYS_REF="address",
                            CURRENCY_CODE="addressNumber",
                            OPERATION="additionalInformation",
                            TRANSACTION_DATE="district",
                            CITY="city",
                            STATE="state",
                            COMMENTS="zipCode")
        return [data]


class TestInvoiceController(unittest.TestCase):
    def get_app(self, session_maker=Mock()):
        blueprint = Blueprint('app')
        blueprint.add_route(Invoice.as_view(session_maker), '/invoice')
        blueprint.add_route(InvoiceInstance.as_view(session_maker), '/invoice/<invoice_id>')

        @blueprint.middleware('request')
        def mid(request):
            return validate_auth_token(request)

        app = Sanic()
        app.blueprint(blueprint)
        return app

    def test_post_missing_request_body(self):
        app = self.get_app()
        request, response = app.test_client.post('/invoice', data=json.dumps({"eventType": 1}))
        assert response.status == 401

    def test_post_request_ok(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        request, response = app.test_client.post('/invoice',
                                                 headers=DEFAULT_HEADER,
                                                 data=json.dumps(REQUEST_BODY))
        assert response.status == 200

    def test_post_request_Exception(self):
        sessionmaker = Mock()
        sessionmaker.return_value.commit.side_effect = Exception("Broken", {}, None)
        app = self.get_app(session_maker=sessionmaker)
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request

        request, response = app.test_client.post('/invoice',
                                                 headers=DEFAULT_HEADER,
                                                 data=json.dumps(REQUEST_BODY))
        assert response.status == 500

    def test_get_request_failed(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        request, response = app.test_client.get('/invoice', headers=DEFAULT_HEADER)
        assert response.status == 500

    def test_get_request_ok(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        RequestManager.get_data_paginated = MockRequestManager.get_data_paginated
        request, response = app.test_client.get('/invoice', headers=DEFAULT_HEADER)
        assert response.status == 200

    def test_get_instance_request_ok(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        RequestManager.get_entry_from_request_with_id = MockRequestManager.get_data_paginated
        request, response = app.test_client.get('/invoice/1', headers=DEFAULT_HEADER)
        assert response.status == 200

    def test_get_instance_request_failed(self):
        app = self.get_app()
        RequestManager.get_org_name_from_request = MockRequestManager.get_org_name_from_request
        request, response = app.test_client.get('/invoice/1', headers=DEFAULT_HEADER)
        assert response.status == 500


if __name__ == '__main__':
    unittest.main()
