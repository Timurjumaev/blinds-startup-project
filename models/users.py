from db import Base
from sqlalchemy import *



class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    username = Column(String(999))
    password = Column(String(999))
    password_hash = Column(String(999))
    role = Column(String(999))
    status = Column(Boolean)
    token = Column(String(999), default='token')