import enum
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from sqlalchemy.orm import relationship
from database import Base
from .base_entity import BaseEntity


class CompanyMode(enum.Enum):
    DRAFT = 'D'
    PUBLISHED = 'P'


class Company(BaseEntity, Base):
    __tablename__ = "companies"

    name = Column(String)
    description = Column(String)
    mode = Column(Enum(CompanyMode), nullable=False, default=CompanyMode.DRAFT)
    rating = Column(SmallInteger, nullable=False, default=0)
    
    users = relationship("User")
