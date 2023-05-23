from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.materials import Materials
from models.orders import Orders
from models.stages import Stages
from models.users import Users


class Trades(Base):
    __tablename__ = "trades"
    id = Column(Integer, autoincrement=True, primary_key=True)
    material_id = Column(Integer)
    width = Column(Numeric)
    height = Column(Numeric)
    stage_id = Column(Integer)
    status = Column(String(10))
    comment = Column(String(999))
    order_id = Column(Integer)
    user_id = Column(Integer)

    stage = relationship('Stages', foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == Trades.stage_id))

    material = relationship('Materials', foreign_keys=[material_id],
                        primaryjoin=lambda: and_(Materials.id == Trades.material_id))

    order = relationship('Orders', foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Trades.order_id))

    user = relationship('Users', foreign_keys=[user_id],
                         primaryjoin=lambda: and_(Users.id == Trades.user_id))
