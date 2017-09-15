from sqlalchemy import Column, String, UniqueConstraint, Numeric, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InvoiceModel(Base):
    __tablename__ = 'XXSTN_ELECTRONIC_INV_INTERF'
    ID = Column(Integer, primary_key=True)
    ORG_ID = Column(String)
    CNPJ_CPF = Column(String, nullable=False)
    AMOUNT = Column(Numeric, nullable=False)
    ORIG_SYS_REF = Column(Numeric, nullable=False)
    CURRENCY_CODE = Column(String)
    OPERATION = Column(Numeric, nullable=False)
    TRANSACTION_DATE = Column(Date)
    CITY = Column(String)
    STATE = Column(String)
    ORG_CODE = Column(String)
    COMMENTS = Column(String)

    UniqueConstraint(ORG_ID, ORIG_SYS_REF, OPERATION)
