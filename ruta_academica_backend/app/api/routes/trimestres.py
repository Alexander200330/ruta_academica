from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.trimestre import Trimestre
from app.models.pensum import Pensum
from app.schemas.trimestre import (
    TrimestreCreate,
    TrimestreInDB,
    TrimestreWithAsignaturas,
)

router = APIRouter()


@router.get("/", response_model=List[TrimestreInDB])
def get_trimestres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener todos los trimestres
    """
    trimestres = db.query(Trimestre).offset(skip).limit(limit).all()
    return trimestres


@router.post("/", response_model=TrimestreInDB, status_code=status.HTTP_201_CREATED)
def create_trimestre(trimestre: TrimestreCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo trimestre
    """
    pensum = db.query(Pensum).filter(Pensum.id == trimestre.pensum_id).first()
    if not pensum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró pensum con ID {trimestre.pensum_id}",
        )

    db_trimestre = (
        db.query(Trimestre)
        .filter(
            Trimestre.numero == trimestre.numero,
            Trimestre.pensum_id == trimestre.pensum_id,
        )
        .first()
    )

    if db_trimestre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un trimestre con el número {trimestre.numero} para este pensum",
        )

    db_trimestre = Trimestre(**trimestre.dict())
    db.add(db_trimestre)
    db.commit()
    db.refresh(db_trimestre)
    return db_trimestre


@router.get("/by-pensum/{pensum_id}", response_model=List[TrimestreInDB])
def get_trimestres_by_pensum(pensum_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los trimestres de un pensum específico
    """
    pensum = db.query(Pensum).filter(Pensum.id == pensum_id).first()
    if not pensum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró pensum con ID {pensum_id}",
        )

    trimestres = db.query(Trimestre).filter(Trimestre.pensum_id == pensum_id).all()
    return trimestres


@router.get("/{trimestre_id}", response_model=TrimestreWithAsignaturas)
def get_trimestre_with_asignaturas(trimestre_id: int, db: Session = Depends(get_db)):
    """
    Obtener un trimestre por su ID, incluyendo sus asignaturas
    """
    db_trimestre = db.query(Trimestre).filter(Trimestre.id == trimestre_id).first()

    if not db_trimestre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró trimestre con ID {trimestre_id}",
        )

    return db_trimestre
