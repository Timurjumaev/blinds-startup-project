from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.collactions import Collactions




class Mechanisms(Base):
    __tablename__ = "mechanisms"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    comment = Column(String(999))
    collaction_id = Column(Integer)
    olchov = Column(String(999))


    collaction = relationship('Collactions', foreign_keys=[collaction_id],
    primaryjoin=lambda: and_(Collactions.id == Mechanisms.collaction_id))