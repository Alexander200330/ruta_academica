import networkx as nx
from typing import Dict, List, Tuple, Any, Set
from collections import deque


class AsignaturaGrafo:
    """
    Clase para manejar el grafo de asignaturas y sus prerrequisitos.
    """

    def __init__(self):
        self.prerrequisitos_graph = nx.DiGraph()
        self.corequisitos_graph = nx.Graph()
        self.combined_graph = nx.DiGraph()

    def add_asignatura(
        self, asignatura_id: int, asignatura_data: Dict[str, Any]
    ) -> None:
        """
        Agrega una asignatura al grafo.

        Args:
            asignatura_id: ID de la asignatura
            asignatura_data: Datos de la asignatura (nombre, código, etc.)
        """
        self.prerrequisitos_graph.add_node(asignatura_id, **asignatura_data)
        self.corequisitos_graph.add_node(asignatura_id, **asignatura_data)
        self.combined_graph.add_node(asignatura_id, **asignatura_data)

    def add_prerequisito(self, asignatura_id: int, prerequisito_id: int) -> None:
        """
        Agrega un prerrequisito entre dos asignaturas.

        Args:
            asignatura_id: ID de la asignatura
            prerequisito_id: ID del prerrequisito

        Nota: La dirección de la arista es: prerequisito -> asignatura
              Esto significa que el prerrequisito debe ser cursado antes de la asignatura
        """
        self.prerrequisitos_graph.add_edge(prerequisito_id, asignatura_id)
        self.combined_graph.add_edge(
            prerequisito_id, asignatura_id, tipo="prerequisito"
        )

    def add_corequisito(self, asignatura_id: int, corequisito_id: int) -> None:
        """
        Agrega un corequisito entre dos asignaturas.

        Args:
            asignatura_id: ID de la asignatura
            corequisito_id: ID del corequisito

        Nota: Los corequisitos son bidireccionales (no dirigidos)
              Esto significa que ambas asignaturas deben cursarse simultáneamente
        """
        self.corequisitos_graph.add_edge(asignatura_id, corequisito_id)
        self.combined_graph.add_edge(asignatura_id, corequisito_id, tipo="corequisito")
        self.combined_graph.add_edge(corequisito_id, asignatura_id, tipo="corequisito")

    def get_all_prerequisitos_bfs(
        self, asignatura_id: int
    ) -> List[Tuple[int, Dict[str, Any]]]:
        """
        Obtiene todos los prerrequisitos de una asignatura utilizando BFS,
        incluyendo prerrequisitos indirectos.

        Args:
            asignatura_id: ID de la asignatura

        Returns:
            Lista de tuplas (id_prerrequisito, datos) para todos los prerrequisitos necesarios
        """
        if asignatura_id not in self.prerrequisitos_graph.nodes:
            return []

        visited = set()
        all_prerequisites = []
        queue = deque([asignatura_id])

        while queue:
            current_id = queue.popleft()

            if current_id != asignatura_id:
                pre_data = self.prerrequisitos_graph.nodes[current_id]
                all_prerequisites.append((current_id, pre_data))

            for pre_id in self.prerrequisitos_graph.predecessors(current_id):
                if pre_id not in visited:
                    visited.add(pre_id)
                    queue.append(pre_id)

        all_required_ids = set(prereq_id for prereq_id, _ in all_prerequisites)
        additional_coreqs = []

        for pre_id, _ in all_prerequisites:
            for co_id in self.corequisitos_graph.neighbors(pre_id):
                if co_id not in all_required_ids and co_id != asignatura_id:
                    all_required_ids.add(co_id)
                    co_data = self.corequisitos_graph.nodes[co_id]
                    additional_coreqs.append((co_id, co_data))

        all_prerequisites.extend(additional_coreqs)

        return all_prerequisites

    def get_direct_prerequisitos(
        self, asignatura_id: int
    ) -> List[Tuple[int, Dict[str, Any]]]:
        """
        Obtiene solo los prerrequisitos directos de una asignatura.

        Args:
            asignatura_id: ID de la asignatura

        Returns:
            Lista de tuplas (id_prerrequisito, datos) para los prerrequisitos directos
        """
        if asignatura_id not in self.prerrequisitos_graph.nodes:
            return []

        prerequisitos = []
        for pre_id in self.prerrequisitos_graph.predecessors(asignatura_id):
            pre_data = self.prerrequisitos_graph.nodes[pre_id]
            prerequisitos.append((pre_id, pre_data))

        return prerequisitos

    def get_corequisitos(self, asignatura_id: int) -> List[Tuple[int, Dict[str, Any]]]:
        """
        Obtiene los corequisitos de una asignatura.

        Args:
            asignatura_id: ID de la asignatura

        Returns:
            Lista de tuplas (id_corequisito, datos) para todos los corequisitos
        """
        if asignatura_id not in self.corequisitos_graph.nodes:
            return []

        corequisitos = []
        for co_id in self.corequisitos_graph.neighbors(asignatura_id):
            co_data = self.corequisitos_graph.nodes[co_id]
            corequisitos.append((co_id, co_data))

        return corequisitos

    def has_cycle_bfs(self) -> bool:
        """
        Detecta si hay ciclos en el grafo de prerrequisitos utilizando BFS.

        El enfoque es utilizar el algoritmo de ordenamiento topológico con BFS.
        Si al final no todos los nodos son visitados, significa que hay ciclos.

        Returns:
            True si hay ciclos, False en caso contrario
        """
        in_degree = {node: 0 for node in self.prerrequisitos_graph.nodes()}
        for node in self.prerrequisitos_graph.nodes():
            for successor in self.prerrequisitos_graph.successors(node):
                in_degree[successor] += 1

        queue = deque([node for node, degree in in_degree.items() if degree == 0])

        visited_count = 0

        while queue:
            current = queue.popleft()
            visited_count += 1

            for neighbor in self.prerrequisitos_graph.successors(current):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count != len(self.prerrequisitos_graph.nodes())

    def get_cycles_bfs(self) -> List[List[int]]:
        """
        Obtiene los ciclos en el grafo de prerrequisitos utilizando BFS.

        Esta implementación detecta los ciclos encontrando los nodos
        que no pueden ser incluidos en un ordenamiento topológico y
        luego busca los ciclos específicos con BFS adicionales.

        Returns:
            Lista de ciclos, donde cada ciclo es una lista de IDs de asignaturas
        """
        in_degree = {node: 0 for node in self.prerrequisitos_graph.nodes()}
        for node in self.prerrequisitos_graph.nodes():
            for successor in self.prerrequisitos_graph.successors(node):
                in_degree[successor] += 1

        queue = deque([node for node, degree in in_degree.items() if degree == 0])

        topological_sorted = []

        while queue:
            current = queue.popleft()
            topological_sorted.append(current)

            for neighbor in self.prerrequisitos_graph.successors(current):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        nodes_in_cycles = set(self.prerrequisitos_graph.nodes()) - set(
            topological_sorted
        )

        all_cycles = []

        for start_node in nodes_in_cycles:
            queue = deque([(start_node, [start_node])])

            while queue:
                node, path = queue.popleft()

                for successor in self.prerrequisitos_graph.successors(node):
                    if successor in path:
                        cycle_start = path.index(successor)
                        cycle = path[cycle_start:] + [successor]
                        if cycle not in all_cycles:
                            all_cycles.append(cycle)
                    elif successor in nodes_in_cycles:
                        new_path = path + [successor]
                        queue.append((successor, new_path))

        return all_cycles

    def has_cycle(self) -> bool:
        """
        Detecta si hay ciclos en el grafo de prerrequisitos.
        Usa la implementación BFS.

        Returns:
            True si hay ciclos, False en caso contrario
        """
        return self.has_cycle_bfs()

    def get_cycles(self) -> List[List[int]]:
        """
        Obtiene los ciclos en el grafo de prerrequisitos.
        Usa la implementación BFS.

        Returns:
            Lista de ciclos, donde cada ciclo es una lista de IDs de asignaturas
        """
        return self.get_cycles_bfs()
