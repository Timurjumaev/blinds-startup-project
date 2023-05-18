from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from models.customers import Customers
from models.suppliers import Suppliers
from models.users import Users
from models.warehouses import Warehouses


class Phones(Base):
    __tablename__ = "phones"
    id = Column(Integer, autoincrement=True, primary_key=True)
    number = Column(String(999))
    comment = Column(String(999))
    source = Column(String(999))
    source_id = Column(Integer)
    user_id = Column(Integer)


    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Phones.user_id))

    this_user = relationship('Users', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Users.id == Phones.source_id, Phones.source == "user"), backref=backref("phones"))

    customer = relationship('Customers', foreign_keys=[source_id],
                         primaryjoin=lambda: and_(Customers.id == Phones.source_id, Phones.source == "customer"), backref=("phones"))

    supplier = relationship('Suppliers', foreign_keys=[source_id],
                             primaryjoin=lambda: and_(Suppliers.id == Phones.source_id, Phones.source == "supplier"),
                             backref=backref("phones"))

    warehouse = relationship('Warehouses', foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Warehouses.id == Phones.source_id, Phones.source == "warehouse"),
                            backref=backref("phones"))