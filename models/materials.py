from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from models.collactions import Collactions
from models.uploaded_files import Uploaded_files


class Materials(Base):
    __tablename__ = "materials"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    comment = Column(String(999))
    collaction_id = Column(Integer)

    collaction = relationship('Collactions', foreign_keys=[collaction_id],
                              primaryjoin=lambda: and_(Collactions.id == Materials.collaction_id))

    files = relationship("Uploaded_files", foreign_keys=[id], primaryjoin=lambda:
                         and_(Uploaded_files.source_id == Materials.id, Uploaded_files.source == "material"))
