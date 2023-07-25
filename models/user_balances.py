from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from models.users import Users
from models.currencies import Currencies


class User_balances(Base):
    __tablename__ = "user_balances"
    id = Column(Integer, autoincrement=True, primary_key=True)
    balance = Column(Numeric)
    currency_id = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    currency = relationship('Currencies', foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == User_balances.currency_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == User_balances.user_id), backref="balansi")
