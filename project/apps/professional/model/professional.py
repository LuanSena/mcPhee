from sqlalchemy.ext.automap import automap_base

from utils.metadata import metadata

Base = automap_base(metadata=metadata)
Base.prepare()


class ProfessionalModel():
    def __init__(self, name=None,
                 address_number=None,
                 document=None,
                 occupation=None,
                 rotation=None,
                 cep=None,
                 user_id=None, professional_id=None):
        self.user_id = user_id
        self.professional_id = professional_id
        self.name = name
        self.address_number = address_number
        self.document = document
        self.occupation = occupation
        self.rotation = rotation
        self.cep = cep

    def add_new(self, session):
        UserModel = Base.classes.USER
        ProfessionalModel = Base.classes.PROFESSIONAL

        new_user = UserModel(username=self.name,
                             addressNumber=self.address_number,
                             document=self.document)
        session.add(new_user)
        session.flush()
        self.user_id = new_user.userID

        new_professional = ProfessionalModel(userID=new_user.userID,
                                             occupation=self.occupation,
                                             rotation=self.rotation)
        session.add(new_professional)
        session.flush()
        self.professional_id = new_professional.professionalID

    def get_by_professional_id(self, session, pid):
        UserModel = Base.classes.USER
        ProfessionalModel = Base.classes.PROFESSIONAL

        result = session.query(ProfessionalModel, UserModel) \
            .filter(ProfessionalModel.userID == UserModel.userID) \
            .filter(ProfessionalModel.professionalID == int(pid)).one()

        self.user_id = result.USER.userID
        self.professional_id = result.PROFESSIONAL.professionalID
        self.name = result.USER.username
        self.address_number = result.USER.addressNumber
        self.document = result.USER.document
        self.occupation = result.PROFESSIONAL.occupation
        self.rotation = result.PROFESSIONAL.rotation

    def get_paginated(self, session, page, page_size):
        UserModel = Base.classes.USER
        ProfessionalModel = Base.classes.PROFESSIONAL

        result_list = list()
        for result in session.query(ProfessionalModel, UserModel).filter(ProfessionalModel.userID == UserModel.userID)\
                             .order_by(UserModel.userID.asc()).offset(page * page_size).limit(page_size):
            new_professional = ProfessionalModel(
                user_id=result.USER.userID,
                professional_id=result.PROFESSIONAL.professionalID,
                name=result.USER.username,
                address_number=result.USER.addressNumber,
                document=result.USER.document,
                occupation=result.PROFESSIONAL.occupation,
                rotation=result.PROFESSIONAL.rotation)
            result_list.append(new_professional)
        return result_list