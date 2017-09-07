from sanic import Sanic

from apps.customer.urls import InvoiceCustomerBP
from apps.invoice.urls import InvoiceBP
from database import orm_db_conn


def get_app():
    app = Sanic()
    session = orm_db_conn.get_session()

    invoice = InvoiceBP(session)
    customer = InvoiceCustomerBP(session)
    app.blueprint(customer.blueprint)
    app.blueprint(invoice.blueprint)
    return app
