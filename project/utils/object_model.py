from utils.metadata import ENGINE, user
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper


# Base = declarative_base()


class UserModel():
    def __init__(self, name, address_number):
        self.username = name
        self.addressNumber = address_number

if __name__ == "__main__":
    mapper(UserModel, user)
    # new_user = UserModel(name = "luan", address_number = "195")
    session_maker = sessionmaker(bind=ENGINE)
    session = session_maker()
    # session.add(new_user)
    # session.commit()

    for row in session.query(UserModel).filter(UserModel.username == "luan"):
        print(row.userID, row.username)