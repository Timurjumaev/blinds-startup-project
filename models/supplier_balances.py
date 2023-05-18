from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.suppliers import Suppliers
from models.currencies import Currencies



class Supplier_balances(Base):
    __tablename__ = "supplier_balances"
    id = Column(Integer, autoincrement=True, primary_key=True)
    balance = Column(Numeric)
    currency_id = Column(Integer)
    supplier_id = Column(Integer)


    currency = relationship('Currencies', foreign_keys=[currency_id],
    primaryjoin=lambda: and_(Currencies.id == Supplier_balances.currency_id))

    supplier = relationship('Suppliers', foreign_keys=[supplier_id],
    primaryjoin=lambda: and_(Suppliers.id == Supplier_balances.supplier_id))
