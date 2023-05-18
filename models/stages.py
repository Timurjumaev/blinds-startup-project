from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.categories import Categories




class Stages(Base):
    __tablename__ = "stages"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    comment = Column(String(999))
    category_id = Column(Integer)
    number = Column(Integer)


    category = relationship('Categories', foreign_keys=[category_id],
    primaryjoin=lambda: and_(Categories.id == Stages.category_id))