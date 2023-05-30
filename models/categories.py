from db import Base
from sqlalchemy import *



class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    width_norm = Column(Numeric)
    height_norm = Column(Numeric)
    width_max = Column(Numeric)
    height_max = Column(Numeric)
