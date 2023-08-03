from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.mechanisms import Mechanisms
from models.trades import Trades


class Trade_mechanisms(Base):
    __tablename__ = "trade_mechanisms"
    id = Column(Integer, autoincrement=True, primary_key=True)
    trade_id = Column(Integer)
    mechanism_id = Column(Integer)
    quantity = Column(Integer)
    branch_id = Column(Integer)

    mechanism = relationship("Mechanisms", foreign_keys=[mechanism_id],
                             primaryjoin=lambda: and_(Mechanisms.id == Trade_mechanisms.mechanism_id))

    trade = relationship('Trades', foreign_keys=[trade_id],
                         primaryjoin=lambda: and_(Trades.id == Trade_mechanisms.trade_id), backref="trade_mechanism")


