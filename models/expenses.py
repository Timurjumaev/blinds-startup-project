from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from models.currencies import Currencies
from models.kassas import Kassas
from models.suppliers import Suppliers
from models.users import Users


class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer, autoincrement=True, primary_key=True)
    money = Column(Numeric)
    currency_id = Column(Integer)
    source = Column(String(999))
    source_id = Column(Integer)
    time = Column(DateTime)
    user_id = Column(Integer)
    kassa_id = Column(Integer)
    comment = Column(String(999))
    updelstatus = Column(Boolean)

    currency = relationship('Currencies', foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Expenses.currency_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Expenses.user_id))

    kassa = relationship('Kassas', foreign_keys=[kassa_id],
                         primaryjoin=lambda: and_(Kassas.id == Expenses.kassa_id))

    source_user = relationship('Users', foreign_keys=[source_id],
                               primaryjoin=lambda: and_(Users.id == Expenses.source_id,
                                                        Expenses.source == "user"))

    source_supplier = relationship('Suppliers', foreign_keys=[source_id],
                                   primaryjoin=lambda: and_(Suppliers.id == Expenses.source_id,
                                                            Expenses.source == "supplier"))


