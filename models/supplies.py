from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.currencies import Currencies
from models.suppliers import Suppliers
from models.users import Users



class Supplies(Base):
    __tablename__ = "supplies"
    id = Column(Integer, autoincrement=True, primary_key=True)
    material_id = Column(Integer)
    mechanism_id = Column(Integer)
    quantity = Column(Numeric)
    price = Column(Numeric)
    currency_id = Column(Integer)
    supplier_id = Column(Integer)
    cr_time = Column(DateTime)
    up_time = Column(DateTime)
    user_id1 = Column(Integer)
    status = Column(Boolean)
    user_id2 = Column(Integer)


    material = relationship('Materials', foreign_keys=[material_id],
    primaryjoin=lambda: and_(Materials.id == Supplies.material_id))

    mechanism = relationship('Mechanisms', foreign_keys=[mechanism_id],
    primaryjoin=lambda: and_(Mechanisms.id == Supplies.mechanism_id))

    currency = relationship('Currencies', foreign_keys=[currency_id],
    primaryjoin=lambda: and_(Currencies.id == Supplies.currency_id))

    supplier = relationship('Suppliers', foreign_keys=[supplier_id],
    primaryjoin=lambda: and_(Suppliers.id == Supplies.supplier_id))

    user1 = relationship('Users', foreign_keys=[user_id1],
    primaryjoin=lambda: and_(Users.id == Supplies.user_id1))

    user2 = relationship('Users', foreign_keys=[user_id2],
    primaryjoin=lambda: and_(Users.id == Supplies.user_id2))
