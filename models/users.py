from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from models.uploaded_files import Uploaded_files


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
    branch_id = Column(Integer)

    files = relationship("Uploaded_files", foreign_keys=[id], primaryjoin=lambda:
                         and_(Uploaded_files.source_id == Users.id, Uploaded_files.source == "user"))
