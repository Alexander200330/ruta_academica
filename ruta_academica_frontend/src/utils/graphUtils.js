/**
 * Utilidades para el procesamiento y visualización de grafos de asignaturas
 */

/**
 * Convierte la estructura de niveles topológicos en una estructura
 * de árbol para facilitar la visualización jerárquica
 * 
 * @param {Object} data - Datos de la ruta académica
 * @returns {Object} Estructura de árbol para visualización
 */
export const convertToTreeStructure = (data) => {
    if (!data || !data.niveles_topologicos) {
      return null;
    }
    
    // Crear un mapa de todas las asignaturas
    const allNodes = {};
    
    // Incluir asignatura objetivo
    allNodes[data.asignatura_objetivo.id] = {
      id: data.asignatura_objetivo.id,
      codigo: data.asignatura_objetivo.codigo,
      nombre: data.asignatura_objetivo.nombre,
      creditos: data.asignatura_objetivo.creditos,
      trimestre: data.asignatura_objetivo.trimestre,
      nivel: "objetivo",
      children: []
    };
    
    // Incluir todas las asignaturas de los niveles
    Object.entries(data.niveles_topologicos).forEach(([nivel, asignaturas]) => {
      asignaturas.forEach(asig => {
        allNodes[asig.id] = {
          id: asig.id,
          codigo: asig.codigo,
          nombre: asig.nombre,
          creditos: asig.creditos,
          trimestre: asig.trimestre,
          nivel: parseInt(nivel),
          children: []
        };
      });
    });
    
    // Construir la estructura de árbol (de abajo hacia arriba)
    Object.entries(data.estructura_dependencias).forEach(([asigId, dependencias]) => {
      const asignatura = allNodes[asigId];
      if (!asignatura) return;
      
      // Añadir prerrequisitos como hijos
      dependencias.prerrequisitos_directos.forEach(preId => {
        const prerequisito = allNodes[preId];
        if (prerequisito) {
          asignatura.children.push(prerequisito);
        }
      });
    });
    
    // El objetivo es la raíz del árbol
    return allNodes[data.asignatura_objetivo.id];
  };
  
  /**
   * Calcula la distribución óptima de nodos en el grafo para la visualización
   * 
   * @param {Object} data - Datos de la ruta académica
   * @returns {Object} Coordenadas para cada nodo
   */
  export const calculateOptimalLayout = (data) => {
    if (!data || !data.niveles_topologicos) {
      return {};
    }
    
    const layout = {};
    const niveles = Object.keys(data.niveles_topologicos).length;
    const maxNodesPerLevel = Math.max(
      ...Object.values(data.niveles_topologicos).map(nivel => nivel.length)
    );
    
    // Establecer posición para objetivo
    layout[data.asignatura_objetivo.id] = {
      x: niveles * 200,
      y: 300
    };
    
    // Establecer posiciones para cada nivel
    Object.entries(data.niveles_topologicos).forEach(([nivelIdx, asignaturas]) => {
      const nivel = parseInt(nivelIdx);
      const x = nivel * 200;
      
      asignaturas.forEach((asig, idx) => {
        const totalNodos = asignaturas.length;
        const espaciado = 600 / (totalNodos + 1);
        const y = (idx + 1) * espaciado;
        
        layout[asig.id] = { x, y };
      });
    });
    
    return layout;
  };
  
  /**
   * Detecta ciclos en la estructura de dependencias
   * 
   * @param {Object} data - Datos de la ruta académica
   * @returns {Array} Lista de ciclos detectados
   */
  export const detectCycles = (data) => {
    if (!data || !data.estructura_dependencias) {
      return [];
    }
    
    // Implementación de detección de ciclos usando DFS
    const visited = new Set();
    const stack = new Set();
    const cycles = [];
    
    const dfs = (nodeId, path = []) => {
      if (stack.has(nodeId)) {
        // Ciclo detectado
        const cycleStart = path.findIndex(id => id === nodeId);
        if (cycleStart >= 0) {
          cycles.push(path.slice(cycleStart).concat(nodeId));
        }
        return;
      }
      
      if (visited.has(nodeId)) {
        return;
      }
      
      visited.add(nodeId);
      stack.add(nodeId);
      path.push(nodeId);
      
      if (data.estructura_dependencias[nodeId]) {
        data.estructura_dependencias[nodeId].prerrequisitos_directos.forEach(preId => {
          dfs(preId, [...path]);
        });
      }
      
      stack.delete(nodeId);
    };
    
    // Iniciar DFS desde cada nodo
    Object.keys(data.estructura_dependencias).forEach(nodeId => {
      if (!visited.has(parseInt(nodeId))) {
        dfs(parseInt(nodeId));
      }
    });
    
    return cycles;
  };
  
  export default {
    convertToTreeStructure,
    calculateOptimalLayout,
    detectCycles
  };