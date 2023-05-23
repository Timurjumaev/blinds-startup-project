from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.trades import Trades
from models.mechanisms import Mechanisms


class Trade_mechanisms(Base):
    __tablename__ = "trade_mechanisms"
    id = Column(Integer, autoincrement=True, primary_key=True)
    trade_id = Column(Integer)
    mechanism_id = Column(Integer)
    width = Column(Numeric)
    quantity = Column(Integer)

    trade = relationship("Trades", foreign_keys=[trade_id],
                         primaryjoin=lambda: and_(Trades.id == Trade_mechanisms.trade_id))

    mechanism = relationship("Mechanisms", foreign_keys=[mechanism_id],
                             primaryjoin=lambda: and_(Mechanisms.id == Trade_mechanisms.mechanism_id))


