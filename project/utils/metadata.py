from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Text, Date

# def migrate_db():
ENGINE = create_engine('sqlite:///test.db', echo=False)
# engine = create_engine('sqlite:////home/luan/Downloads/SQLiteStudio/dbs/mcphee', echo=True)


metadata = MetaData()

user = Table(
    'USER', metadata,
    Column('userID', Integer, primary_key=True, autoincrement=True),
    Column('username', String(16), nullable=False),
    Column('document', String, nullable=False),
    Column("addressNumber", String)
)

login = Table(
    'LOGIN', metadata,
    Column('loginID', Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("USER.userID"), nullable=False),
    Column('emailaddress', String(60), key='email'),
    Column('password', String(20), nullable=False)
)

contact = Table(
    "CONTACT", metadata,
    Column("contactID", Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("USER.userID"), nullable=False),
    Column("type", String),
    Column("contact_type", String),
    Column("contact", String)
)

address = Table(
    "ADDRESS", metadata,
    Column("addressID", Integer, primary_key=True),
    Column("cep", String),
    Column("city", String),
    Column("state", String),
    Column("name", String),
    Column("adjunct", String)  # useful information / reference point
)

address_user = Table(
    "ADDRESS_USER", metadata,
    Column('addressID', Integer, ForeignKey("ADDRESS.addressID"), nullable=False),
    Column('userID', Integer, ForeignKey("USER.userID"), nullable=False)
)

professional = Table(
    'PROFESSIONAL', metadata,
    Column("professionalID", Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("USER.userID"), nullable=False),
    Column("occupation", String, nullable=False),
    Column("rotation", String)
)

responsible = Table(  # student responsable
    "RESPONSIBLE", metadata,
    Column("responsibleID", Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("USER.userID"), nullable=False),
    Column("relationship", String)
)

student = Table(
    "STUDENT", metadata,
    Column("studentID", Integer, primary_key=True),
    Column('userID', Integer, ForeignKey("USER.userID"), nullable=False),
    Column("anotations", Text)
)

responsible_student = Table(
    "RESPONSIBLESTUDENT", metadata,
    Column('responsibleID', Integer, ForeignKey("RESPONSIBLE.responsibleID"), nullable=False),
    Column('studentID', Integer, ForeignKey("STUDENT.studentID"), nullable=False)
)

school = Table(
    "SCHOOL", metadata,
    Column("schoolID", Integer, primary_key=True),
    Column("name", String),
    Column("Owner", String),  # head director
    Column('addressID', Integer, ForeignKey("ADDRESS.addressID"), nullable=False)
)

school_anotations = Table(
    "SCHOOL_ANOTATIONS", metadata,
    Column("anotationsID", Integer, primary_key=True),
    Column("date", Date),
    Column("anotation", Text)  # observations
)

professional_school = Table(
    "PROFESSIONAL_SCHOOL", metadata,
    Column('professionalID', Integer, ForeignKey("PROFESSIONAL.professionalID"), nullable=False),
    Column('schoolID', Integer, ForeignKey("SCHOOL.schoolID"), nullable=False)
)

school_class = Table(
    "CLASS", metadata,
    Column("classID", Integer, primary_key=True),
    Column('schoolID', Integer, ForeignKey("SCHOOL.schoolID"), nullable=False),
    Column("rotation", String),  # shift
    Column("name", String)
)

class_professional = Table(
    "CLASS_PROFESSIONAL", metadata,
    Column('professionalID', Integer, ForeignKey("PROFESSIONAL.professionalID"), nullable=False),
    Column('classID', Integer, ForeignKey("CLASS.classID"), nullable=False)
)

# http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.MetaData.create_all

if __name__ == "__main__":
    # migrate_db()
    metadata.drop_all(ENGINE)
    metadata.create_all(ENGINE)