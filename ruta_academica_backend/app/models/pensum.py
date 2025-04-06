from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base import Base


class Pensum(Base):
    __tablename__ = "pensums"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    fecha_aprobacion = Column(Date)
    resolucion = Column(String)
    carrera_id = Column(Integer, ForeignKey("carreras.id"))
    carrera = relationship("Carrera", back_populates="pensums")
    trimestres = relationship("Trimestre", back_populates="pensum")
