from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from models.mechanisms import Mechanisms
from models.users import Users


class Standart_mechanisms(Base):
    __tablename__ = "standart_mechanisms"
    id = Column(Integer, autoincrement=True, primary_key=True)
    mechanism_id = Column(Integer)
    width = Column(Numeric)
    quantity = Column(Integer)
    user_id = Column(Integer)

    mechanism = relationship("Mechanisms", foreign_keys=[mechanism_id],
                         primaryjoin=lambda: and_(Mechanisms.id == Standart_mechanisms.mechanism_id))

    user = relationship("Users", foreign_keys=[user_id],
                             primaryjoin=lambda: and_(Users.id == Standart_mechanisms.user_id))
