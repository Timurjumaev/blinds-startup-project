from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.collactions import Collactions
from models.uploaded_files import Uploaded_files


class Mechanisms(Base):
    __tablename__ = "mechanisms"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    comment = Column(String(999))
    collaction_id = Column(Integer)
    olchov = Column(String(999))
    branch_id = Column(Integer)

    collaction = relationship('Collactions', foreign_keys=[collaction_id],
                              primaryjoin=lambda: and_(Collactions.id == Mechanisms.collaction_id))

    files = relationship("Uploaded_files", foreign_keys=[id], primaryjoin=lambda:
                         and_(Uploaded_files.source_id == Mechanisms.id, Uploaded_files.source == "mechanism"))
