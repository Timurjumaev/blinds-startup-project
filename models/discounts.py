from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.users import Users


class Discounts(Base):
    __tablename__ = "discounts"
    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String(999))
    percent = Column(Numeric)
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                              primaryjoin=lambda: and_(Users.id == Discounts.user_id))