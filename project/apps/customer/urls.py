from sanic import Blueprint
from sanic.response import json

from apps.customer.controller.customer_controller import Customer, CustomerInstance
from utils.auth import validate_auth_token


class InvoiceCustomerBP:
    def __init__(self, session_maker):
        blueprint = Blueprint('customer')

        @blueprint.middleware('request')
        def mid(request):
            return validate_auth_token(request)

        blueprint.add_route(Customer.as_view(session_maker), '/customer')
        blueprint.add_route(CustomerInstance.as_view(session_maker), '/customer/<customer_id>')
        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
