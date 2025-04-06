from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Trimestre(Base):
    __tablename__ = "trimestres"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer)
    pensum_id = Column(Integer, ForeignKey("pensums.id"))
    pensum = relationship("Pensum", back_populates="trimestres")
    asignaturas = relationship("AsignaturaTrimestre", back_populates="trimestre")
