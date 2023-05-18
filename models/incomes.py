from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.currencies import Currencies
from models.kassas import Kassas
from models.users import Users


class Incomes(Base):
    __tablename__ = "incomes"
    id = Column(Integer, autoincrement=True, primary_key=True)
    money = Column(Numeric)
    currency_id = Column(Integer)
    source = Column(String(999))
    source_id = Column(Integer)
    time = Column(DateTime)
    user_id = Column(Integer)
    kassa_id = Column(Integer)
    comment = Column(String(999))

    currency = relationship('Currencies', foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Incomes.currency_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Incomes.user_id))

    kassa = relationship('Kassas', foreign_keys=[kassa_id],
                            primaryjoin=lambda: and_(Kassas.id == Incomes.kassa_id))


