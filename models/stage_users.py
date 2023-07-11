from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from models.currencies import Currencies
from models.users import Users
from models.stages import Stages


class Stage_users(Base):
    __tablename__ = "stage_users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    kpi = Column(Numeric)
    currency_id = Column(Integer)
    stage_id = Column(Integer)
    branch_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Stage_users.user_id))

    stage = relationship('Stages', foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == Stage_users.stage_id))

    currency = relationship('Currencies', foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Stage_users.currency_id))
