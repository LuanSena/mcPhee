from sanic import Blueprint

from apps.invoice.controller.invoice_controller import Invoice, InvoiceInstance


class InvoiceBP:
    def __init__(self, session_maker):
        blueprint = Blueprint('invoice')

        blueprint.add_route(Invoice.as_view(session_maker), '/invoice')
        blueprint.add_route(InvoiceInstance.as_view(session_maker), '/invoice/<invoice_id>')

        self.blueprint = blueprint

    def blueprint(self):
        return self.blueprint
