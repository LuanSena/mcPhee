from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from utils.metadata import ENGINE, metadata

Base = automap_base(metadata=metadata)
Base.prepare()

UserModel = Base.classes.USER

class TestModel():
    def __init__(self):
        self.model = Base.classes.USER

    def set_model(self, username, addressNumber):
        user = self.model(username=username, addressNumber=addressNumber)
        return user

if __name__ == "__main__":
    # new_user = UserModel(username="luan", addressNumber="195")
    new_user = TestModel()
    new_user = new_user.set_model(username="fulano", addressNumber="555")
    session_maker = sessionmaker(bind=ENGINE)
    session = session_maker()
    session.add(new_user)
    session.commit()

    for row in session.query(UserModel): #.filter(UserModel.username == "luan"):
        print(row.userID, row.username)
