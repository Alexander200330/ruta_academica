from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.asignatura import Asignatura
from app.models.pensum import Pensum
from app.services.grafo_service import GrafoService


router = APIRouter()


@router.get("/ruta/{asignatura_id}", response_model=Dict)
def get_ruta_academica(
    asignatura_id: int, pensum_id: Optional[int] = None, db: Session = Depends(get_db)
):
    """
    Obtiene la ruta académica completa para llegar a una asignatura por su ID,
    es decir, todas las asignaturas que deben ser cursadas previamente,
    organizadas por niveles topológicos para indicar el orden recomendado.

    Args:
        asignatura_id: ID de la asignatura objetivo
        pensum_id: ID del pensum (opcional, para filtrar por pensum)
    """
    asignatura = db.query(Asignatura).filter(Asignatura.id == asignatura_id).first()
    if not asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró asignatura con ID {asignatura_id}",
        )

    if pensum_id:
        pensum = db.query(Pensum).filter(Pensum.id == pensum_id).first()
        if not pensum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró pensum con ID {pensum_id}",
            )

    prerrequisitos = GrafoService.get_prerequisitos(db, asignatura_id, pensum_id)

    grafo = GrafoService.build_asignaturas_graph(db, pensum_id)
    niveles = GrafoService.get_niveles_topologicos(grafo, asignatura_id)

    if grafo.has_cycle():
        ciclos = grafo.get_cycles()
        ciclos_info = []

        for ciclo in ciclos:
            ciclo_asignaturas = []
            for asig_id in ciclo:
                asig = db.query(Asignatura).filter(Asignatura.id == asig_id).first()
                if asig:
                    ciclo_asignaturas.append(
                        {"id": asig.id, "codigo": asig.codigo, "nombre": asig.nombre}
                    )
            ciclos_info.append(ciclo_asignaturas)

        return {
            "error": "Se detectaron ciclos en los prerrequisitos",
            "ciclos": ciclos_info,
            "asignatura_objetivo": {
                "id": asignatura.id,
                "codigo": asignatura.codigo,
                "nombre": asignatura.nombre,
            },
        }

    result = {
        "asignatura_objetivo": {
            "id": asignatura.id,
            "codigo": asignatura.codigo,
            "nombre": asignatura.nombre,
            "creditos": asignatura.creditos,
            "req_creditos": asignatura.req_creditos,
            "trimestre": prerrequisitos["asignatura"].get("trimestre", None),
            "pensum_id": prerrequisitos["asignatura"].get("pensum_id", None),
        },
        "prerrequisitos_directos": prerrequisitos["prerrequisitos_directos"],
        "todos_prerrequisitos": prerrequisitos["todos_prerrequisitos"],
        "corequisitos": prerrequisitos["corequisitos"],
        "total_asignaturas_previas": len(prerrequisitos["todos_prerrequisitos"]),
        "creditos_requeridos_total": sum(
            materia["creditos"] for materia in prerrequisitos["todos_prerrequisitos"]
        ),
        "niveles_topologicos": niveles,
        "estructura_dependencias": _construir_estructura_dependencias(
            db, prerrequisitos["todos_prerrequisitos"]
        ),
    }

    return result


@router.get("/ruta-por-codigo/{codigo}", response_model=Dict)
def get_ruta_academica_por_codigo(
    codigo: str, pensum_id: Optional[int] = None, db: Session = Depends(get_db)
):
    """
    Obtiene la ruta académica completa para llegar a una asignatura por su código,
    es decir, todas las asignaturas que deben ser cursadas previamente,
    organizadas por niveles topológicos para indicar el orden recomendado.

    Args:
        codigo: Código de la asignatura objetivo (ej. "MAT101")
        pensum_id: ID del pensum (opcional, para filtrar por pensum)
    """
    codigo = codigo.upper()

    if pensum_id:
        pensum = db.query(Pensum).filter(Pensum.id == pensum_id).first()
        if not pensum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró pensum con ID {pensum_id}",
            )

    if pensum_id:
        from app.models.trimestre import Trimestre
        from app.models.asignatura import AsignaturaTrimestre
        asignatura_query = (
            db.query(Asignatura)
            .join(
                AsignaturaTrimestre, Asignatura.id == AsignaturaTrimestre.asignatura_id
            )
            .join(Trimestre, AsignaturaTrimestre.trimestre_id == Trimestre.id)
            .filter(Asignatura.codigo == codigo)
            .filter(Trimestre.pensum_id == pensum_id)
        )

        asignatura = asignatura_query.first()

        if not asignatura:
            asig_general = (
                db.query(Asignatura).filter(Asignatura.codigo == codigo).first()
            )
            if asig_general:
                return {
                    "error": f"La asignatura {codigo} existe en la base de datos pero no está asociada al pensum {pensum_id}",
                    "asignatura_objetivo": {
                        "id": asig_general.id,
                        "codigo": asig_general.codigo,
                        "nombre": asig_general.nombre,
                    },
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró asignatura con código {codigo}",
                )
    else:
        asignatura = db.query(Asignatura).filter(Asignatura.codigo == codigo).first()
        if not asignatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró asignatura con código {codigo}",
            )

    prerequisitos_info = GrafoService.get_prerequisitos(db, asignatura.id, pensum_id)

    if "error" in prerequisitos_info:
        return {
            "error": prerequisitos_info["error"],
            "asignatura_objetivo": {
                "id": asignatura.id,
                "codigo": asignatura.codigo,
                "nombre": asignatura.nombre,
            },
        }

    grafo = GrafoService.build_asignaturas_graph(db, pensum_id)

    if asignatura.id not in grafo.prerrequisitos_graph.nodes:
        return {
            "error": f"La asignatura {codigo} ({asignatura.id}) no está incluida en el grafo para el pensum {pensum_id}",
            "asignatura_objetivo": {
                "id": asignatura.id,
                "codigo": asignatura.codigo,
                "nombre": asignatura.nombre,
            },
        }

    niveles = GrafoService.get_niveles_topologicos(grafo, asignatura.id)

    if grafo.has_cycle():
        ciclos = grafo.get_cycles()
        ciclos_info = []

        for ciclo in ciclos:
            ciclo_asignaturas = []
            for asig_id in ciclo:
                asig = db.query(Asignatura).filter(Asignatura.id == asig_id).first()
                if asig:
                    ciclo_asignaturas.append(
                        {"id": asig.id, "codigo": asig.codigo, "nombre": asig.nombre}
                    )
            ciclos_info.append(ciclo_asignaturas)

        return {
            "error": "Se detectaron ciclos en los prerrequisitos",
            "ciclos": ciclos_info,
            "asignatura_objetivo": {
                "id": asignatura.id,
                "codigo": asignatura.codigo,
                "nombre": asignatura.nombre,
            },
        }

    trimestre_info = prerequisitos_info["asignatura"].get("trimestre", None)
    pensum_info = prerequisitos_info["asignatura"].get("pensum_id", None)

    if (trimestre_info is None or pensum_info is None) and pensum_id:
        from app.models.trimestre import Trimestre
        from app.models.asignatura import AsignaturaTrimestre

        trimestre_data = (
            db.query(Trimestre.numero)
            .join(AsignaturaTrimestre, AsignaturaTrimestre.trimestre_id == Trimestre.id)
            .filter(AsignaturaTrimestre.asignatura_id == asignatura.id)
            .filter(Trimestre.pensum_id == pensum_id)
            .first()
        )

        if trimestre_data:
            trimestre_info = trimestre_data[0]
            pensum_info = pensum_id

    result = {
        "asignatura_objetivo": {
            "id": asignatura.id,
            "codigo": asignatura.codigo,
            "nombre": asignatura.nombre,
            "creditos": asignatura.creditos,
            "req_creditos": asignatura.req_creditos,
            "trimestre": trimestre_info,
            "pensum_id": pensum_info,
        },
        "prerrequisitos_directos": prerequisitos_info["prerrequisitos_directos"],
        "todos_prerrequisitos": prerequisitos_info["todos_prerrequisitos"],
        "corequisitos": prerequisitos_info["corequisitos"],
        "total_asignaturas_previas": len(prerequisitos_info["todos_prerrequisitos"]),
        "creditos_requeridos_total": sum(
            materia["creditos"]
            for materia in prerequisitos_info["todos_prerrequisitos"]
        ),
        "niveles_topologicos": niveles,
        "estructura_dependencias": _construir_estructura_dependencias(
            db, prerequisitos_info["todos_prerrequisitos"]
        ),
    }

    return result


@router.get("/asignaturas-por-nivel/{pensum_id}", response_model=Dict)
def get_asignaturas_por_nivel(pensum_id: int, db: Session = Depends(get_db)):
    """
    Organiza las asignaturas de un pensum por niveles según sus prerrequisitos.
    Una asignatura está en el nivel N si su prerrequisito más profundo está en el nivel N-1.

    Args:
        pensum_id: ID del pensum
    """
    pensum = db.query(Pensum).filter(Pensum.id == pensum_id).first()
    if not pensum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró pensum con ID {pensum_id}",
        )

    graph = GrafoService.build_asignaturas_graph(db, pensum_id)

    from app.models.trimestre import Trimestre
    from app.models.asignatura import AsignaturaTrimestre

    asignaturas = (
        db.query(Asignatura)
        .join(AsignaturaTrimestre, Asignatura.id == AsignaturaTrimestre.asignatura_id)
        .join(Trimestre, AsignaturaTrimestre.trimestre_id == Trimestre.id)
        .filter(Trimestre.pensum_id == pensum_id)
        .all()
    )

    asignatura_trimestres = {}
    for asignatura in asignaturas:
        trimestre_info = (
            db.query(Trimestre.numero)
            .join(AsignaturaTrimestre, Trimestre.id == AsignaturaTrimestre.trimestre_id)
            .filter(AsignaturaTrimestre.asignatura_id == asignatura.id)
            .filter(Trimestre.pensum_id == pensum_id)
            .first()
        )

        if trimestre_info:
            asignatura_trimestres[asignatura.id] = trimestre_info[0]
        else:
            asignatura_trimestres[asignatura.id] = None

    levels = {}
    assigned = set()

    level0 = []
    for asignatura in asignaturas:
        if not asignatura.prerequisitos:
            level0.append(
                {
                    "id": asignatura.id,
                    "codigo": asignatura.codigo,
                    "nombre": asignatura.nombre,
                    "creditos": asignatura.creditos,
                    "trimestre": asignatura_trimestres.get(asignatura.id),
                }
            )
            assigned.add(asignatura.id)

    levels[0] = level0

    level = 1
    while len(assigned) < len(asignaturas):
        current_level = []

        for asignatura in asignaturas:
            if asignatura.id in assigned:
                continue

            all_prereqs_assigned = all(
                pre.id in assigned for pre in asignatura.prerequisitos
            )

            if all_prereqs_assigned:
                current_level.append(
                    {
                        "id": asignatura.id,
                        "codigo": asignatura.codigo,
                        "nombre": asignatura.nombre,
                        "creditos": asignatura.creditos,
                        "trimestre": asignatura_trimestres.get(asignatura.id),
                    }
                )
                assigned.add(asignatura.id)

        if not current_level:
            break

        levels[level] = current_level
        level += 1

    no_asignadas = []
    for asignatura in asignaturas:
        if asignatura.id not in assigned:
            no_asignadas.append(
                {
                    "id": asignatura.id,
                    "codigo": asignatura.codigo,
                    "nombre": asignatura.nombre,
                    "creditos": asignatura.creditos,
                    "trimestre": asignatura_trimestres.get(asignatura.id),
                }
            )

    result = {
        "niveles": levels,
        "no_asignadas": no_asignadas,
        "total_niveles": len(levels),
        "total_asignaturas": len(asignaturas),
        "asignaturas_asignadas": len(assigned),
        "asignaturas_no_asignadas": len(no_asignadas),
    }

    return result


def _construir_estructura_dependencias(db: Session, prerrequisitos: List[Dict]) -> Dict:
    """
    Construye una estructura que muestra las dependencias entre las asignaturas prerrequisitos.

    Args:
        db: Sesión de base de datos
        prerrequisitos: Lista de prerrequisitos

    Returns:
        Diccionario con la estructura de dependencias
    """
    estructura = {}

    for pre in prerrequisitos:
        asignatura_id = pre["id"]
        asignatura = db.query(Asignatura).filter(Asignatura.id == asignatura_id).first()

        if asignatura:
            pre_ids = [p.id for p in asignatura.prerequisitos]

            co_ids = [c.id for c in asignatura.corequisitos]

            from app.models.trimestre import Trimestre
            from app.models.asignatura import AsignaturaTrimestre

            trimestre_info = (
                db.query(Trimestre.numero, Trimestre.pensum_id)
                .join(
                    AsignaturaTrimestre,
                    AsignaturaTrimestre.trimestre_id == Trimestre.id,
                )
                .filter(AsignaturaTrimestre.asignatura_id == asignatura_id)
                .first()
            )

            trimestre_numero = None
            pensum_id = None
            if trimestre_info:
                trimestre_numero = trimestre_info[0]
                pensum_id = trimestre_info[1]

            estructura[asignatura_id] = {
                "codigo": asignatura.codigo,
                "nombre": asignatura.nombre,
                "prerrequisitos_directos": pre_ids,
                "corequisitos": co_ids,
                "trimestre": trimestre_numero,
                "pensum_id": pensum_id,
            }

    return estructura
