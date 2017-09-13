from sqlalchemy.ext.automap import automap_base

from utils.metadata import metadata

Base = automap_base(metadata=metadata)
Base.prepare()


class ProfessionalModel():
    def __init__(self, name, address_number, document, occupation, rotation, cep,
                 user_id=None, professional_id=None):
        self.user_id=user_id
        self.professional_id=professional_id
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
