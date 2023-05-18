from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from models.categories import Categories



class Collactions(Base):
    __tablename__ = "collactions"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    category_id = Column(Integer)


    category = relationship('Categories', foreign_keys=[category_id],
    primaryjoin=lambda: and_(Categories.id == Collactions.category_id))