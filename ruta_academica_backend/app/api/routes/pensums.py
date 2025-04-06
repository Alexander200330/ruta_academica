from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.pensum import Pensum
from app.models.carrera import Carrera
from app.schemas.pensum import PensumCreate, PensumInDB

router = APIRouter()


@router.get("/", response_model=List[PensumInDB])
def get_pensums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener todos los pensums
    """
    pensums = db.query(Pensum).offset(skip).limit(limit).all()
    return pensums


@router.post("/", response_model=PensumInDB, status_code=status.HTTP_201_CREATED)
def create_pensum(pensum: PensumCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo pensum
    """
    carrera = db.query(Carrera).filter(Carrera.id == pensum.carrera_id).first()
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró carrera con ID {pensum.carrera_id}",
        )

    db_pensum = db.query(Pensum).filter(Pensum.codigo == pensum.codigo).first()
    if db_pensum:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un pensum con el código {pensum.codigo}",
        )

    db_pensum = Pensum(**pensum.dict())
    db.add(db_pensum)
    db.commit()
    db.refresh(db_pensum)
    return db_pensum


@router.get("/by-carrera/{carrera_id}", response_model=List[PensumInDB])
def get_pensums_by_carrera(carrera_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los pensums de una carrera específica
    """
    carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró carrera con ID {carrera_id}",
        )

    pensums = db.query(Pensum).filter(Pensum.carrera_id == carrera_id).all()
    return pensums


@router.get("/{pensum_id}", response_model=PensumInDB)
def get_pensum(pensum_id: int, db: Session = Depends(get_db)):
    """
    Obtener un pensum por su ID
    """
    db_pensum = db.query(Pensum).filter(Pensum.id == pensum_id).first()
    if not db_pensum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró pensum con ID {pensum_id}",
        )
    return db_pensum
