from sanic import Sanic

from apps.professional.urls import ProfessionalBP
from database import orm_db_conn


def get_app():
    app = Sanic()
    session = orm_db_conn.get_session()

    # invoice = InvoiceBP(session)
    # customer = InvoiceCustomerBP(session)
    professional = ProfessionalBP(session)
    # app.blueprint(customer.blueprint)
    # app.blueprint(invoice.blueprint)
    app.blueprint(professional.blueprint)
    return app
