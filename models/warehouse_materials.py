from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.currencies import Currencies
from models.warehouses import Warehouses
from models.cells import Cells



class Warehouse_materials(Base):
    __tablename__ = "warehouse_materials"
    id = Column(Integer, autoincrement=True, primary_key=True)
    material_id = Column(Integer)
    width = Column(Numeric)
    height = Column(Numeric)
    mechanism_id = Column(Integer)
    quantity = Column(Numeric)
    price = Column(Numeric)
    currency_id = Column(Integer)
    warehouse_id = Column(Integer)
    cell_id = Column(Integer)

    material = relationship('Materials', foreign_keys=[material_id],
                            primaryjoin=lambda: and_(Materials.id == Warehouse_materials.material_id))

    mechanism = relationship('Mechanisms', foreign_keys=[mechanism_id],
                             primaryjoin=lambda: and_(Mechanisms.id == Warehouse_materials.mechanism_id))

    currency = relationship('Currencies', foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Warehouse_materials.currency_id))

    warehouse = relationship('Warehouses', foreign_keys=[warehouse_id],
                             primaryjoin=lambda: and_(Warehouses.id == Warehouse_materials.warehouse_id))

    cell = relationship('Cells', foreign_keys=[cell_id],
                        primaryjoin=lambda: and_(Cells.id == Warehouse_materials.cell_id))
