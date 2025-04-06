from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.carrera import Carrera
from app.schemas.carrera import CarreraCreate, CarreraInDB

router = APIRouter()


@router.get("/", response_model=List[CarreraInDB])
def get_carreras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener todas las carreras
    """
    carreras = db.query(Carrera).offset(skip).limit(limit).all()
    return carreras


@router.post("/", response_model=CarreraInDB, status_code=status.HTTP_201_CREATED)
def create_carrera(carrera: CarreraCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva carrera
    """
    db_carrera = db.query(Carrera).filter(Carrera.nombre == carrera.nombre).first()
    if db_carrera:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una carrera con el nombre {carrera.nombre}",
        )

    db_carrera = Carrera(**carrera.dict())
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera


@router.get("/{carrera_id}", response_model=CarreraInDB)
def get_carrera(carrera_id: int, db: Session = Depends(get_db)):
    """
    Obtener una carrera por su ID
    """
    db_carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()
    if not db_carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró carrera con ID {carrera_id}",
        )
    return db_carrera
