import enum
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from sqlalchemy.orm import relationship
from database import Base
from .base_entity import BaseEntity


class TaskMode(enum.Enum):
    ACTIVE = 'A'
    UNACTIVE = 'U'


class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary = Column(String)
    description = Column(String)
    status = Column(Enum(TaskMode), nullable=False, default=TaskMode.ACTIVE)
    priority = Column(SmallInteger, nullable=False, default=0)   
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=True) 
