from typing import List
from pydantic import BaseModel
from app.schemas.asignatura import AsignaturaInDB


class TrimestreBase(BaseModel):
    numero: int
    pensum_id: int


class TrimestreCreate(TrimestreBase):
    pass


class TrimestreInDB(TrimestreBase):
    id: int

    class Config:
        from_attributes = True


class TrimestreWithAsignaturas(TrimestreInDB):
    asignaturas: List[AsignaturaInDB] = []

    class Config:
        from_attributes = True
