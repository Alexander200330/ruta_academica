from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.base import Base

prerequisito = Table(
    "prerequisitos",
    Base.metadata,
    Column("asignatura_id", Integer, ForeignKey("asignaturas.id"), primary_key=True),
    Column("prerequisito_id", Integer, ForeignKey("asignaturas.id"), primary_key=True),
)

corequisito = Table(
    "corequisitos",
    Base.metadata,
    Column("asignatura_id", Integer, ForeignKey("asignaturas.id"), primary_key=True),
    Column("corequisito_id", Integer, ForeignKey("asignaturas.id"), primary_key=True),
)


class Asignatura(Base):
    __tablename__ = "asignaturas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True)
    nombre = Column(String)
    creditos = Column(Integer)
    req_creditos = Column(Integer, nullable=True)
    trimestres = relationship("AsignaturaTrimestre", back_populates="asignatura")
    prerequisitos = relationship(
        "Asignatura",
        secondary=prerequisito,
        primaryjoin=(prerequisito.c.asignatura_id == id),
        secondaryjoin=(prerequisito.c.prerequisito_id == id),
        backref="es_prerequisito_de",
    )
    corequisitos = relationship(
        "Asignatura",
        secondary=corequisito,
        primaryjoin=(corequisito.c.asignatura_id == id),
        secondaryjoin=(corequisito.c.corequisito_id == id),
        backref="es_corequisito_de",
    )


class AsignaturaTrimestre(Base):
    __tablename__ = "asignaturas_trimestres"

    asignatura_id = Column(Integer, ForeignKey("asignaturas.id"), primary_key=True)
    trimestre_id = Column(Integer, ForeignKey("trimestres.id"), primary_key=True)
    asignatura = relationship("Asignatura", back_populates="trimestres")
    trimestre = relationship("Trimestre", back_populates="asignaturas")
