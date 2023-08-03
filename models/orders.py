from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.customers import Customers
from models.users import Users


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, autoincrement=True, primary_key=True)
    time = Column(DateTime)
    customer_id = Column(Integer)
    status = Column(String(999))
    user_id = Column(Integer)
    delivery_date = Column(Date)
    discount = Column(Numeric, default=0)
    money_status = Column(Boolean, default=False)
    branch_id = Column(Integer)

    customer = relationship('Customers', foreign_keys=[customer_id],
                            primaryjoin=lambda: and_(Customers.id == Orders.customer_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Orders.user_id))