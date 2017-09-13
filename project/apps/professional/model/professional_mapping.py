from sqlalchemy.ext.automap import automap_base

from utils.metadata import metadata

Base = automap_base(metadata=metadata)
Base.prepare()


class ProfessionalModel():
    def __init__(self, name, address_number, document, email, occupation, rotation, cep,
                 user_id=None, professional_id=None):
        self.user_id=user_id
        self.professional_id=professional_id
        self.name = name
        self.address_number = address_number
        self.document = document
        self.email = email
        self.occupation = occupation
        self.rotation = rotation
        self.cep = cep

    def add(self):
        pass
