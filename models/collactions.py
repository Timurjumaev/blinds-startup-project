from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from models.categories import Categories
from models.uploaded_files import Uploaded_files


class Collactions(Base):
    __tablename__ = "collactions"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    category_id = Column(Integer)
    branch_id = Column(Integer)

    category = relationship('Categories', foreign_keys=[category_id],
                            primaryjoin=lambda: and_(Categories.id == Collactions.category_id))

    files = relationship("Uploaded_files", foreign_keys=[id], primaryjoin=lambda:
                         and_(Uploaded_files.source_id == Collactions.id, Uploaded_files.source == "collaction"))

