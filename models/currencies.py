from db import Base
from sqlalchemy import *


class Currencies(Base):
    __tablename__ = "currencies"
    id = Column(Integer, autoincrement=True, primary_key=True)
    price = Column(Numeric)
    currency = Column(String(999))
    branch_id = Column(Integer)
