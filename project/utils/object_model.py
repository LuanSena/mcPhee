import random

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from utils.metadata import ENGINE, metadata

Base = automap_base(metadata=metadata)
Base.prepare()

UserModel = Base.classes.USER
ProfessionalModel = Base.classes.PROFESSIONAL

if __name__ == "__main__":
    session_maker = sessionmaker(bind=ENGINE)
    session = session_maker()

    new_user = UserModel(username="luan", addressNumber="195", document=random.randint(0, 999999999))
    session.add(new_user)
    session.flush()

    new_professional = ProfessionalModel(userID=new_user.userID, occupation="admin")
    session.add(new_professional)
    session.commit()

    for row in session.query(ProfessionalModel, UserModel).filter(ProfessionalModel.userID == UserModel.userID):
        print(row.PROFESSIONAL.userID,
              row.USER.username,
              row.PROFESSIONAL.professionalID,
              row.PROFESSIONAL.occupation,
              row.USER.document)
