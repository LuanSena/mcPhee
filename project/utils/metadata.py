from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Text

engine = create_engine('sqlite:///:memory:', echo=True)

metadata = MetaData()

user = Table(
    'USER', metadata,
    Column('userID', Integer, primary_key=True),
    Column('username', String(16), nullable=False),
    Column("addressNumber")
)

login = Table(
    'LOGIN', metadata,
    Column('loginID', Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("user.userID"), nullable=False),
    Column('emailaddress', String(60), key='email'),
    Column('password', String(20), nullable=False)
)

contact = Table(
    "CONTACT", metadata,
    Column("contactID", Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("user.userID"), nullable=False),
    Column("type", String),
    Column("contact", String)
)

address = Table(
    "ADDRESS", metadata,
    Column("addressID", Integer, primary_key=True),
    Column("cep", String),
    Column("city", String),
    Column("state", String),
    Column("name", String),
    Column("adjunct", String)
)

address_user = Table(
    "ADDRESS_USER", metadata,
    Column('addressID', Integer, ForeignKey("ADDRESS.addressID"), nullable=False),
    Column('userID', Integer, ForeignKey("USER.userID"), nullable=False)
)

manager = Table(
    'MANAGER', metadata,
    Column('managerID', Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("user.userID"), nullable=False),
    Column('post', String, nullable=False)
)

professional = Table(
    'PROFESSIONAL', metadata,
    Column("professionalID", Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("user.userID"), nullable=False),
    Column("post", String, nullable=False),
    Column("rotation", String)
)

responsible = Table(
    "RESPONSIBLE", metadata,
    Column("responsableID", Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("user.userID"), nullable=False),
    Column("relationship", String)
)

student = Table(
    "STUDENT", metadata,
    Column("studentID", Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("user.userID"), nullable=False),
    Column("anotations", Text)
)

responsible_student = Table(
    "RESPONSIBLESTUDENT", metadata,
    Column('responsableID', Integer, ForeignKey("RESPONSIBLE.responsibleID"), nullable=False),
    Column('studentID', Integer, ForeignKey("STUDENT.studentID"), nullable=False)
)

metadata.create_all(engine)

# http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.MetaData.create_all
