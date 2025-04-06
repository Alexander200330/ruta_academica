from typing import Optional
from datetime import date
from pydantic import BaseModel


class PensumBase(BaseModel):
    codigo: str
    fecha_aprobacion: Optional[date] = None
    resolucion: Optional[str] = None
    carrera_id: int


class PensumCreate(PensumBase):
    pass


class PensumInDB(PensumBase):
    id: int

    class Config:
        from_attributes = True
