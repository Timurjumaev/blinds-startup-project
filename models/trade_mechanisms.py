from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.mechanisms import Mechanisms


class Trade_mechanisms(Base):
    __tablename__ = "trade_mechanisms"
    id = Column(Integer, autoincrement=True, primary_key=True)
    trade_id = Column(Integer)
    mechanism_id = Column(Integer)
    quantity = Column(Integer)
    branch_id = Column(Integer)

    mechanism = relationship("Mechanisms", foreign_keys=[mechanism_id],
                             primaryjoin=lambda: and_(Mechanisms.id == Trade_mechanisms.mechanism_id))


