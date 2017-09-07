from sqlalchemy import Column, String, UniqueConstraint, Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CustomerModel(Base):

    __tablename__ = 'XXSTN_CUSTOMER_INTERFACE'

    #ORG
    ORG_NAME = Column(String)
    ORG_ID = Column(Numeric)

    #Customer
    ID = Column(Integer, primary_key=True)
    CNPJ_CPF = Column(String(255))
    CUSTOMER_NAME = Column(String)
    ADDRESS = Column(String)
    ADDRESS_NUMBER = Column(String)
    ADDITIONAL_INFORMATION = Column(String)
    DISTRICT = Column(String)
    CITY = Column(String)
    STATE = Column(String)
    ZIP_CODE = Column(String)
    EMAIL_ADDRESS = Column(String)
    CONTACT_NAME = Column(String)
    PHONE_NUMBER = Column(String)
    STATUS = Column(String)
    MESSAGE = Column(String)
    EMAIL_INVOICE = Column(String)
    CITY_IBGE_CODE = Column(String)
    STATUS_EMAIL_INVOICE = Column(String)
    COUNTRY = Column(String)

    UniqueConstraint(ORG_NAME, CNPJ_CPF)
