from typing import Optional
from pydantic import BaseModel


class CarreraBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CarreraCreate(CarreraBase):
    pass


class CarreraInDB(CarreraBase):
    id: int

    class Config:
        from_attributes = True
