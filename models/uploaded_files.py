from db import Base
from sqlalchemy import *


class Uploaded_files(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, autoincrement=True, primary_key=True)
    file = Column(Text)
    source = Column(String(999))
    source_id = Column(Integer)
