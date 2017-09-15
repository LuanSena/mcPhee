from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OrgModel(Base):
    __tablename__ = 'XXSTN_HR_OPERATING_UNITS'

    ORGANIZATION_ID = Column(Integer, primary_key=True)
    NAME = Column(String)
