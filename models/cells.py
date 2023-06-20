from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.warehouses import Warehouses


class Cells(Base):
    __tablename__ = "cells"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name1 = Column(String(999))
    name2 = Column(String(999))
    warehouse_id = Column(Integer)
    branch_id = Column(Integer)

    warehouse = relationship('Warehouses', foreign_keys=[warehouse_id],
                             primaryjoin=lambda: and_(Warehouses.id == Cells.warehouse_id))
