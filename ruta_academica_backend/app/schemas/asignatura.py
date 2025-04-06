from typing import List, Optional
from pydantic import BaseModel


class AsignaturaBase(BaseModel):
    codigo: str
    nombre: str
    creditos: int
    req_creditos: Optional[int] = None


class AsignaturaCreate(AsignaturaBase):
    pass


class AsignaturaTrimestre(BaseModel):
    asignatura_id: int
    trimestre_id: int

    class Config:
        from_attributes = True


class AsignaturaWithRelations(AsignaturaBase):
    id: int
    prerequisitos_ids: Optional[List[int]] = []
    corequisitos_ids: Optional[List[int]] = []

    class Config:
        from_attributes = True


class AsignaturaInDB(AsignaturaBase):
    id: int

    class Config:
        from_attributes = True


class AsignaturaUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    creditos: Optional[int] = None
    req_creditos: Optional[int] = None
