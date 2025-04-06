from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.api.dependencies import get_db
from app.models.asignatura import Asignatura, AsignaturaTrimestre
from app.models.trimestre import Trimestre
from app.schemas.asignatura import (
    AsignaturaCreate,
    AsignaturaUpdate,
    AsignaturaInDB,
    AsignaturaTrimestre as AsignaturaTrimestreSchema,
    AsignaturaWithRelations,
)

router = APIRouter()


@router.get("/", response_model=List[AsignaturaWithRelations])
def get_asignaturas(skip: int = 0, limit: int = 300, db: Session = Depends(get_db)):
    """
    Obtener todas las asignaturas con sus prerrequisitos y correquisitos
    """
    asignaturas = db.query(Asignatura).offset(skip).limit(limit).all()

    result = []
    for asignatura in asignaturas:
        prerequisitos_ids = [p.id for p in asignatura.prerequisitos]
        corequisitos_ids = [c.id for c in asignatura.corequisitos]

        result.append(
            {
                **asignatura.__dict__,
                "prerequisitos_ids": prerequisitos_ids,
                "corequisitos_ids": corequisitos_ids,
            }
        )

    return result


@router.post("/", response_model=AsignaturaInDB, status_code=status.HTTP_201_CREATED)
def create_asignatura(asignatura: AsignaturaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva asignatura
    """
    db_asignatura = (
        db.query(Asignatura).filter(Asignatura.codigo == asignatura.codigo).first()
    )
    if db_asignatura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una asignatura con el código {asignatura.codigo}",
        )

    db_asignatura = Asignatura(**asignatura.dict())
    db.add(db_asignatura)
    db.commit()
    db.refresh(db_asignatura)
    return db_asignatura


@router.post("/asignar-trimestre", response_model=AsignaturaTrimestreSchema)
def assign_asignatura_to_trimestre(
    assignment: AsignaturaTrimestreSchema, db: Session = Depends(get_db)
):
    """
    Asignar una asignatura a un trimestre específico
    """
    asignatura = (
        db.query(Asignatura).filter(Asignatura.id == assignment.asignatura_id).first()
    )
    if not asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {assignment.asignatura_id}",
        )

    trimestre = (
        db.query(Trimestre).filter(Trimestre.id == assignment.trimestre_id).first()
    )
    if not trimestre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró trimestre con ID {assignment.trimestre_id}",
        )

    existing = (
        db.query(AsignaturaTrimestre)
        .filter(
            AsignaturaTrimestre.asignatura_id == assignment.asignatura_id,
            AsignaturaTrimestre.trimestre_id == assignment.trimestre_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta asignatura ya está asignada a este trimestre",
        )

    db_assignment = AsignaturaTrimestre(
        asignatura_id=assignment.asignatura_id, trimestre_id=assignment.trimestre_id
    )
    db.add(db_assignment)
    db.commit()

    return assignment


@router.post(
    "/agregar-prerequisito/{asignatura_id}/{prerequisito_id}",
    response_model=AsignaturaWithRelations,
)
def add_prerequisito(
    asignatura_id: int, prerequisito_id: int, db: Session = Depends(get_db)
):
    """
    Agregar un prerrequisito a una asignatura
    """
    asignatura = db.query(Asignatura).filter(Asignatura.id == asignatura_id).first()
    if not asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {asignatura_id}",
        )

    prerequisito = db.query(Asignatura).filter(Asignatura.id == prerequisito_id).first()
    if not prerequisito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {prerequisito_id}",
        )

    if prerequisito not in asignatura.prerequisitos:
        asignatura.prerequisitos.append(prerequisito)
        db.commit()
        db.refresh(asignatura)

    prerequisitos_ids = [p.id for p in asignatura.prerequisitos]
    corequisitos_ids = [c.id for c in asignatura.corequisitos]

    return {
        **asignatura.__dict__,
        "prerequisitos_ids": prerequisitos_ids,
        "corequisitos_ids": corequisitos_ids,
    }


@router.post(
    "/agregar-corequisito/{asignatura_id}/{corequisito_id}",
    response_model=AsignaturaWithRelations,
)
def add_corequisito(
    asignatura_id: int, corequisito_id: int, db: Session = Depends(get_db)
):
    """
    Agregar un correquisito a una asignatura
    """
    asignatura = db.query(Asignatura).filter(Asignatura.id == asignatura_id).first()
    if not asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {asignatura_id}",
        )

    corequisito = db.query(Asignatura).filter(Asignatura.id == corequisito_id).first()
    if not corequisito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {corequisito_id}",
        )

    if corequisito not in asignatura.corequisitos:
        asignatura.corequisitos.append(corequisito)
        db.commit()
        db.refresh(asignatura)

    prerequisitos_ids = [p.id for p in asignatura.prerequisitos]
    corequisitos_ids = [c.id for c in asignatura.corequisitos]

    return {
        **asignatura.__dict__,
        "prerequisitos_ids": prerequisitos_ids,
        "corequisitos_ids": corequisitos_ids,
    }


@router.get("/by-trimestre/{trimestre_id}", response_model=List[AsignaturaInDB])
def get_asignaturas_by_trimestre(trimestre_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las asignaturas de un trimestre específico
    """
    trimestre = db.query(Trimestre).filter(Trimestre.id == trimestre_id).first()
    if not trimestre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró trimestre con ID {trimestre_id}",
        )

    asignaturas = (
        db.query(Asignatura)
        .join(AsignaturaTrimestre, Asignatura.id == AsignaturaTrimestre.asignatura_id)
        .filter(AsignaturaTrimestre.trimestre_id == trimestre_id)
        .all()
    )

    return asignaturas


@router.get("/{asignatura_id}", response_model=AsignaturaWithRelations)
def get_asignatura(asignatura_id: int, db: Session = Depends(get_db)):
    """
    Obtener una asignatura por su ID, incluyendo prerrequisitos y correquisitos
    """
    asignatura = db.query(Asignatura).filter(Asignatura.id == asignatura_id).first()
    if not asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {asignatura_id}",
        )

    prerequisitos_ids = [p.id for p in asignatura.prerequisitos]
    corequisitos_ids = [c.id for c in asignatura.corequisitos]

    return {
        **asignatura.__dict__,
        "prerequisitos_ids": prerequisitos_ids,
        "corequisitos_ids": corequisitos_ids,
    }


@router.put("/{asignatura_id}", response_model=AsignaturaInDB)
def update_asignatura(
    asignatura_id: int, asignatura: AsignaturaUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar una asignatura
    """
    db_asignatura = db.query(Asignatura).filter(Asignatura.id == asignatura_id).first()
    if not db_asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {asignatura_id}",
        )

    update_data = asignatura.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asignatura, key, value)

    db.commit()
    db.refresh(db_asignatura)
    return db_asignatura


@router.delete("/{asignatura_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asignatura(asignatura_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una asignatura
    """
    db_asignatura = db.query(Asignatura).filter(Asignatura.id == asignatura_id).first()
    if not db_asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {asignatura_id}",
        )

    db.delete(db_asignatura)
    db.commit()
    return None
