from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from models.orders import Orders


class Loans(Base):
    __tablename__ = "loans"
    id = Column(Integer, autoincrement=True, primary_key=True)
    money = Column(Numeric)
    residual = Column(Numeric)
    order_id = Column(Integer)
    return_date = Column(Date)
    comment = Column(String(999))

    order = relationship('Orders', foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Loans.order_id))
