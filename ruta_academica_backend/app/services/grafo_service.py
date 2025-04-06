from typing import Dict, List, Optional, Tuple, Any
from sqlalchemy.orm import Session
from collections import deque

from app.models.asignatura import Asignatura
from app.models.pensum import Pensum
from app.models.trimestre import Trimestre
from app.models.asignatura import AsignaturaTrimestre

from app.core.graph import AsignaturaGrafo


class GrafoService:
    @staticmethod
    def build_asignaturas_graph(
        db: Session, pensum_id: Optional[int] = None
    ) -> AsignaturaGrafo:
        """
        Construye el grafo de asignaturas con sus prerrequisitos y corequisitos.

        Args:
            db: Sesión de base de datos
            pensum_id: ID del pensum para filtrar asignaturas (opcional)

        Returns:
            AsignaturaGrafo: Instancia del grafo de asignaturas
        """
        grafo = AsignaturaGrafo()

        if pensum_id:
            from app.models.trimestre import Trimestre
            from app.models.asignatura import AsignaturaTrimestre

            asignaturas = (
                db.query(Asignatura)
                .join(
                    AsignaturaTrimestre,
                    Asignatura.id == AsignaturaTrimestre.asignatura_id,
                )
                .join(Trimestre, AsignaturaTrimestre.trimestre_id == Trimestre.id)
                .filter(Trimestre.pensum_id == pensum_id)
                .distinct()
                .all()
            )
        else:
            asignaturas = db.query(Asignatura).all()

        print(f"Total de asignaturas para el grafo: {len(asignaturas)}")

        for asignatura in asignaturas:
            trimestre_info = None
            if pensum_id:
                from app.models.trimestre import Trimestre

                trimestre_info = (
                    db.query(Trimestre.numero, Trimestre.pensum_id)
                    .join(
                        AsignaturaTrimestre,
                        AsignaturaTrimestre.trimestre_id == Trimestre.id,
                    )
                    .filter(AsignaturaTrimestre.asignatura_id == asignatura.id)
                    .filter(Trimestre.pensum_id == pensum_id)
                    .first()
                )

            asignatura_data = {
                "codigo": asignatura.codigo,
                "nombre": asignatura.nombre,
                "creditos": asignatura.creditos,
                "req_creditos": asignatura.req_creditos,
            }

            if trimestre_info:
                asignatura_data["trimestre"] = trimestre_info[0]
                asignatura_data["pensum_id"] = trimestre_info[1]

            grafo.add_asignatura(asignatura.id, asignatura_data)

        asignatura_ids = [a.id for a in asignaturas]

        for asignatura in asignaturas:
            for prerequisito in asignatura.prerequisitos:
                if prerequisito.id in asignatura_ids:
                    grafo.add_prerequisito(asignatura.id, prerequisito.id)

            for corequisito in asignatura.corequisitos:
                if corequisito.id in asignatura_ids:
                    grafo.add_corequisito(asignatura.id, corequisito.id)

        return grafo

    @staticmethod
    def get_prerequisitos(
        db: Session, asignatura_id: int, pensum_id: Optional[int] = None
    ) -> Dict:
        """
        Obtiene todos los prerrequisitos de una asignatura, tanto directos como indirectos,
        así como sus corequisitos.

        Args:
            db: Sesión de base de datos
            asignatura_id: ID de la asignatura
            pensum_id: ID del pensum (opcional)

        Returns:
            Diccionario con la asignatura, prerrequisitos directos, todos los prerrequisitos y corequisitos
        """
        asignatura = db.query(Asignatura).filter(Asignatura.id == asignatura_id).first()
        if not asignatura:
            return {"error": f"No se encontró asignatura con ID {asignatura_id}"}

        grafo = GrafoService.build_asignaturas_graph(db, pensum_id)

        trimestre_info = None
        if pensum_id:
            trimestre_info = (
                db.query(Trimestre.numero, Trimestre.pensum_id)
                .join(
                    AsignaturaTrimestre,
                    AsignaturaTrimestre.trimestre_id == Trimestre.id,
                )
                .filter(AsignaturaTrimestre.asignatura_id == asignatura_id)
                .filter(Trimestre.pensum_id == pensum_id)
                .first()
            )

        asignatura_data = {
            "id": asignatura.id,
            "codigo": asignatura.codigo,
            "nombre": asignatura.nombre,
            "creditos": asignatura.creditos,
            "req_creditos": asignatura.req_creditos,
        }

        if trimestre_info:
            asignatura_data["trimestre"] = trimestre_info[0]
            asignatura_data["pensum_id"] = trimestre_info[1]

        prerrequisitos_directos = []
        for pre_id, pre_data in grafo.get_direct_prerequisitos(asignatura_id):
            pre_obj = {
                "id": pre_id,
                "codigo": pre_data["codigo"],
                "nombre": pre_data["nombre"],
                "creditos": pre_data["creditos"],
            }

            if "trimestre" in pre_data:
                pre_obj["trimestre"] = pre_data["trimestre"]

            prerrequisitos_directos.append(pre_obj)

        todos_prerrequisitos = []
        for pre_id, pre_data in grafo.get_all_prerequisitos_bfs(asignatura_id):
            pre_obj = {
                "id": pre_id,
                "codigo": pre_data["codigo"],
                "nombre": pre_data["nombre"],
                "creditos": pre_data["creditos"],
            }

            if "trimestre" in pre_data:
                pre_obj["trimestre"] = pre_data["trimestre"]

            todos_prerrequisitos.append(pre_obj)

        corequisitos = []
        for co_id, co_data in grafo.get_corequisitos(asignatura_id):
            co_obj = {
                "id": co_id,
                "codigo": co_data["codigo"],
                "nombre": co_data["nombre"],
                "creditos": co_data["creditos"],
            }

            if "trimestre" in co_data:
                co_obj["trimestre"] = co_data["trimestre"]

            corequisitos.append(co_obj)

        return {
            "asignatura": asignatura_data,
            "prerrequisitos_directos": prerrequisitos_directos,
            "todos_prerrequisitos": todos_prerrequisitos,
            "corequisitos": corequisitos,
        }

    @staticmethod
    def get_niveles_topologicos(
        grafo: AsignaturaGrafo, asignatura_id: int
    ) -> Dict[int, List[Dict]]:
        """
        Organiza los prerrequisitos de una asignatura en niveles topológicos.

        Args:
            grafo: Instancia de AsignaturaGrafo
            asignatura_id: ID de la asignatura objetivo

        Returns:
            Diccionario con niveles topológicos de las asignaturas prerrequisito
        """
        prerrequisitos = [
            pre_id for pre_id, _ in grafo.get_all_prerequisitos_bfs(asignatura_id)
        ]

        nodos = prerrequisitos + [asignatura_id]

        subgrafo = AsignaturaGrafo()

        for nodo_id in nodos:
            if nodo_id in grafo.prerrequisitos_graph.nodes:
                data = grafo.prerrequisitos_graph.nodes[nodo_id]
                subgrafo.add_asignatura(nodo_id, data)

        for nodo_id in nodos:
            if nodo_id in grafo.prerrequisitos_graph.nodes:
                for succ_id in grafo.prerrequisitos_graph.successors(nodo_id):
                    if (
                        succ_id in nodos
                        and succ_id in subgrafo.prerrequisitos_graph.nodes
                    ):
                        subgrafo.add_prerequisito(succ_id, nodo_id)

        if not subgrafo.prerrequisitos_graph.nodes:
            return {}

        in_degree = {node: 0 for node in subgrafo.prerrequisitos_graph.nodes()}

        for node in subgrafo.prerrequisitos_graph.nodes():
            if node in subgrafo.prerrequisitos_graph:
                for successor in subgrafo.prerrequisitos_graph.successors(node):
                    if successor in in_degree:
                        in_degree[successor] += 1

        niveles = {}
        nivel_actual = 0

        queue = deque([node for node, degree in in_degree.items() if degree == 0])

        while queue:
            nivel_nodos = []
            nivel_size = len(queue)

            for _ in range(nivel_size):
                nodo_id = queue.popleft()

                if nodo_id not in subgrafo.prerrequisitos_graph.nodes:
                    continue

                nodo_data = subgrafo.prerrequisitos_graph.nodes[nodo_id]
                nivel_nodos.append(
                    {
                        "id": nodo_id,
                        "codigo": nodo_data["codigo"],
                        "nombre": nodo_data["nombre"],
                        "creditos": nodo_data["creditos"],
                        "trimestre": nodo_data.get("trimestre", None),
                    }
                )

                if nodo_id in subgrafo.prerrequisitos_graph:
                    for succ_id in subgrafo.prerrequisitos_graph.successors(nodo_id):
                        if succ_id in in_degree:
                            in_degree[succ_id] -= 1
                            if in_degree[succ_id] == 0:
                                queue.append(succ_id)

            if nivel_nodos:
                niveles[nivel_actual] = nivel_nodos
                nivel_actual += 1

        return niveles
