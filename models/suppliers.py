from db import Base
from sqlalchemy import *



class Suppliers(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    address = Column(String(999))
    map_long = Column(String(999))
    map_lat = Column(String(999))