from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *

from models.currencies import Currencies
from models.orders import Orders


class Loans(Base):
    __tablename__ = "loans"
    id = Column(Integer, autoincrement=True, primary_key=True)
    money = Column(Numeric)
    currency_id = Column(Integer)
    residual = Column(Numeric)
    order_id = Column(Integer)
    return_date = Column(Date)
    comment = Column(String(999))
    status = Column(Boolean)

    currency = relationship('Currencies', foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Loans.currency_id))

    order = relationship('Orders', foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Loans.order_id))


