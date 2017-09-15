from apps.common.model.tables import OrgModel

PAGE_PARAM_KEY = 'page'


class RequestManager:

    @staticmethod
    def get_page_from_request(request):
        if PAGE_PARAM_KEY in request.args:
            page = int(request.args[PAGE_PARAM_KEY][0])
        else:
            page = 0
        return page

    @staticmethod
    def get_org_name_from_request(request, session):
        for row in session.query(OrgModel).filter(OrgModel.ORGANIZATION_ID == request["company"]):
            name = row.NAME
            return name

    @staticmethod
    def get_entry_from_request_with_id(model, company_id, id_pk, session):
        for row in session.query(model).filter(model.ID == id_pk).filter(model.ORG_ID == company_id):
            return row

    @staticmethod
    def get_data_paginated(model, session, company_id, page, page_size):
        result = session.query(model).filter(model.ORG_ID == company_id).order_by(model.ID.asc()).offset(page * page_size).limit(page_size).all()
        return result
