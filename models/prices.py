from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from models.collactions import Collactions
from models.currencies import Currencies



class Prices(Base):
    __tablename__ = "prices"
    id = Column(Integer, autoincrement=True, primary_key=True)
    price = Column(Numeric)
    currency_id = Column(Integer)
    width1 = Column(Numeric)
    width2 = Column(Numeric)
    height1 = Column(Numeric)
    height2 = Column(Numeric)
    collaction_id = Column(Integer)


    collaction = relationship('Collactions', foreign_keys=[collaction_id],
    primaryjoin=lambda: and_(Collactions.id == Prices.collaction_id))

    currency = relationship('Currencies', foreign_keys=[currency_id],
    primaryjoin=lambda: and_(Currencies.id == Prices.currency_id))
