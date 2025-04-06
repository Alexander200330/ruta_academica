import React, { useEffect, useRef, useState } from 'react';
import { Network } from 'vis-network/standalone';
import { DataSet } from 'vis-data';
import { Card, Button, ButtonGroup, Alert } from 'react-bootstrap';

const GraphVisualization = ({ data }) => {
  const containerRef = useRef(null);
  const networkRef = useRef(null);
  const [view, setView] = useState('tree');
  const [error, setError] = useState(null);
  
  useEffect(() => {
    if (!data || !containerRef.current) return;
    
    try {
      console.log("Iniciando visualización con datos:", data);
      
      // Limpiar cualquier red existente
      if (networkRef.current) {
        networkRef.current.destroy();
        networkRef.current = null;
      }
      
      // Asegurarse de que la estructura de datos tenga lo necesario
      if (!data.asignatura_objetivo) {
        setError('Los datos de la asignatura no contienen información suficiente');
        return;
      }
      
      // Set para verificar IDs únicos
      const usedNodeIds = new Set();
      const usedEdgeIds = new Set();
      
      // Función para generar IDs únicos garantizados
      const generateUniqueId = (prefix, originalId) => {
        let uniqueId;
        do {
          // Combinación de prefijo + originalId + timestamp + número aleatorio
          uniqueId = `${prefix}_${originalId}_${Date.now()}_${Math.floor(Math.random() * 10000)}`;
        } while (usedNodeIds.has(uniqueId));
        
        usedNodeIds.add(uniqueId);
        return uniqueId;
      };
      
      const generateUniqueEdgeId = (prefix, fromId, toId) => {
        let uniqueId;
        do {
          uniqueId = `${prefix}_${fromId}_${toId}_${Math.floor(Math.random() * 10000)}`;
        } while (usedEdgeIds.has(uniqueId));
        
        usedEdgeIds.add(uniqueId);
        return uniqueId;
      };
      
      // Función para colorear según el nivel
      const getColorForLevel = (level) => {
        const colors = [
          '#3498db', // Azul - Nivel 0
          '#2ecc71', // Verde - Nivel 1
          '#f39c12', // Naranja - Nivel 2
          '#9b59b6', // Púrpura - Nivel 3
          '#1abc9c', // Turquesa - Nivel 4
          '#d35400', // Naranja oscuro - Nivel 5
          '#8e44ad', // Púrpura oscuro - Nivel 6
          '#2980b9', // Azul oscuro - Nivel 7+
        ];
        
        return level < colors.length ? colors[level] : colors[colors.length - 1];
      };
      
      // Mapeo de IDs originales a IDs únicos
      const idMap = new Map();
      
      // Preparar los nodos y aristas para el grafo
      const nodes = new DataSet();
      const edges = new DataSet();
      
      // Función para añadir un nodo garantizando un ID único
      const addNode = (originalId, label, options) => {
        // Si el nodo ya fue agregado, retornar su ID único
        if (idMap.has(originalId)) {
          return idMap.get(originalId);
        }
        
        // Generar un ID único para este nodo
        const uniqueId = generateUniqueId('node', originalId);
        idMap.set(originalId, uniqueId);
        
        // Crear el nodo con el ID único
        const nodeData = {
          id: uniqueId,
          label,
          ...options
        };
        
        // Añadir el nodo al dataset
        nodes.add(nodeData);
        
        return uniqueId;
      };
      
      // Función para añadir una arista garantizando un ID único
      const addEdge = (fromOriginalId, toOriginalId, options) => {
        if (!idMap.has(fromOriginalId) || !idMap.has(toOriginalId)) {
          console.warn(`No se puede crear arista: ID original no mapeado`, 
                       fromOriginalId, toOriginalId);
          return;
        }
        
        const fromId = idMap.get(fromOriginalId);
        const toId = idMap.get(toOriginalId);
        
        // Generar un ID único para esta arista
        const uniqueId = generateUniqueEdgeId('edge', fromId, toId);
        
        // Crear la arista con el ID único
        const edgeData = {
          id: uniqueId,
          from: fromId,
          to: toId,
          ...options
        };
        
        // Añadir la arista al dataset
        edges.add(edgeData);
      };
      
      // Procesar los prerrequisitos primero (para que la asignatura objetivo quede arriba)
      const procesarNiveles = () => {
        if (!data.niveles_topologicos || typeof data.niveles_topologicos !== 'object') {
          console.warn("No hay niveles topológicos disponibles o formato inválido");
          return;
        }
        
        // Ordenar los niveles de menor a mayor (0, 1, 2...)
        const nivelesOrdenados = Object.entries(data.niveles_topologicos)
          .sort((a, b) => parseInt(a[0]) - parseInt(b[0]));
        
        nivelesOrdenados.forEach(([nivelIdx, asignaturas]) => {
          if (!Array.isArray(asignaturas)) {
            console.warn(`Nivel ${nivelIdx} no contiene un array válido:`, asignaturas);
            return;
          }
          
          const nivel = parseInt(nivelIdx);
          
          asignaturas.forEach(asignatura => {
            if (!asignatura || !asignatura.id || !asignatura.codigo || !asignatura.nombre) {
              console.warn("Asignatura con datos incompletos:", asignatura);
              return;
            }
            
            addNode(
              asignatura.id,
              `${asignatura.codigo}\n${asignatura.nombre}${asignatura.trimestre ? `\n(Trimestre ${asignatura.trimestre})` : ''}`,
              {
                shape: 'box',
                level: nivel,
                color: {
                  background: getColorForLevel(nivel),
                  border: '#333',
                  highlight: {
                    background: getColorForLevel(nivel),
                    border: '#000'
                  }
                },
                font: { size: 14, face: 'Arial' },
                shadow: true
              }
            );
          });
        });
      };
      
      // Procesar prerrequisitos si no hay niveles
      const procesarPrerrequisitos = () => {
        if (!data.todos_prerrequisitos || !Array.isArray(data.todos_prerrequisitos)) {
          console.warn("No hay prerrequisitos disponibles o formato inválido");
          return;
        }
        
        data.todos_prerrequisitos.forEach((asignatura) => {
          if (!asignatura || !asignatura.id || !asignatura.codigo || !asignatura.nombre) {
            console.warn("Prerrequisito con datos incompletos:", asignatura);
            return;
          }
          
          addNode(
            asignatura.id,
            `${asignatura.codigo}\n${asignatura.nombre}${asignatura.trimestre ? `\n(Trimestre ${asignatura.trimestre})` : ''}`,
            {
              shape: 'box',
              level: 0, // Los niveles se determinarán automáticamente en modo árbol
              color: {
                background: getColorForLevel(0),
                border: '#333',
                highlight: {
                  background: getColorForLevel(0),
                  border: '#000'
                }
              },
              font: { size: 14, face: 'Arial' },
              shadow: true
            }
          );
        });
      };
      
      // Ahora agregamos la asignatura objetivo solo una vez
      const procesarAsignaturaObjetivo = () => {
        addNode(
          data.asignatura_objetivo.id,
          `${data.asignatura_objetivo.codigo}\n${data.asignatura_objetivo.nombre}${data.asignatura_objetivo.trimestre ? `\n(Trimestre ${data.asignatura_objetivo.trimestre})` : ''}`,
          {
            shape: 'box',
            color: {
              background: '#e74c3c', // Color rojo para la asignatura objetivo
              border: '#c0392b',
              highlight: {
                background: '#e74c3c',
                border: '#c0392b'
              }
            },
            font: { color: 'white', size: 14, face: 'Arial', bold: true },
            borderWidth: 2,
            shadow: true
          }
        );
      };
      
      // Procesar conexiones de dependencias
      const procesarDependencias = () => {
        if (!data.estructura_dependencias || typeof data.estructura_dependencias !== 'object') {
          console.warn("No hay estructura de dependencias disponible o formato inválido");
          return false;
        }
        
        let conexionesCreadas = 0;
        
        Object.entries(data.estructura_dependencias).forEach(([asigId, dependencias]) => {
          const asignaturaId = parseInt(asigId);
          
          // Prerrequisitos directos
          if (dependencias.prerrequisitos_directos && Array.isArray(dependencias.prerrequisitos_directos)) {
            dependencias.prerrequisitos_directos.forEach(preId => {
              try {
                // La dirección es: prerrequisito -> asignatura (el prerrequisito apunta a la asignatura)
                addEdge(preId, asignaturaId, {
                  arrows: 'to',
                  color: { color: '#2c3e50', highlight: '#34495e' },
                  width: 2,
                  smooth: { type: 'curvedCW', roundness: 0.2 }
                });
                conexionesCreadas++;
              } catch (error) {
                console.warn(`Error al crear arista prerrequisito: ${preId} -> ${asignaturaId}`, error);
              }
            });
          }
          
          // Corequisitos
          if (dependencias.corequisitos && Array.isArray(dependencias.corequisitos)) {
            dependencias.corequisitos.forEach(coId => {
              try {
                // Verificar si esta arista de corequisito ya fue creada
                // (solo queremos crearla una vez para cada par)
                const idMenor = Math.min(asignaturaId, coId);
                const idMayor = Math.max(asignaturaId, coId);
                const edgeKey = `co_${idMenor}_${idMayor}`;
                if (!usedEdgeIds.has(edgeKey)) {
                  usedEdgeIds.add(edgeKey);
                  
                  // Crear arista bidireccional para corequisitos
                  addEdge(asignaturaId, coId, {
                    arrows: {
                      from: { enabled: false },
                      to: { enabled: false }
                    },
                    color: { color: '#3498db', highlight: '#2980b9' },
                    width: 2,
                    dashes: [5, 5],
                    smooth: { type: 'continuous' }
                  });
                  conexionesCreadas++;
                }
              } catch (error) {
                console.warn(`Error al crear arista corequisito: ${asignaturaId} <-> ${coId}`, error);
              }
            });
          }
        });
        
        return conexionesCreadas > 0;
      };
      
      // Procesar conexiones directas si no hay estructura de dependencias
      const procesarConexionesDirectas = () => {
        if (!data.prerrequisitos_directos || !Array.isArray(data.prerrequisitos_directos)) {
          console.warn("No hay prerrequisitos directos disponibles o formato inválido");
          return false;
        }
        
        let conexionesCreadas = 0;
        
        data.prerrequisitos_directos.forEach(pre => {
          if (!pre || !pre.id) {
            console.warn("Prerrequisito directo con datos incompletos:", pre);
            return;
          }
          
          try {
            // La dirección es: prerrequisito -> asignatura objetivo
            addEdge(pre.id, data.asignatura_objetivo.id, {
              arrows: 'to',
              color: { color: '#2c3e50', highlight: '#34495e' },
              width: 2,
              smooth: { type: 'curvedCW', roundness: 0.2 }
            });
            conexionesCreadas++;
          } catch (error) {
            console.warn(`Error al crear arista directa: ${pre.id} -> ${data.asignatura_objetivo.id}`, error);
          }
        });
        
        return conexionesCreadas > 0;
      };
      
      // Procesar corequisitos directos
      const procesarCorequisitosDirectos = () => {
        if (!data.corequisitos || !Array.isArray(data.corequisitos)) {
          return false;
        }
        
        let conexionesCreadas = 0;
        
        data.corequisitos.forEach(co => {
          if (!co || !co.id) {
            console.warn("Corequisito con datos incompletos:", co);
            return;
          }
          
          try {
            // Crear conectores de corequisitos (líneas punteadas sin flechas)
            addEdge(data.asignatura_objetivo.id, co.id, {
              arrows: {
                from: { enabled: false },
                to: { enabled: false }
              },
              color: { color: '#3498db', highlight: '#2980b9' },
              width: 2,
              dashes: [5, 5],
              smooth: { type: 'continuous' }
            });
            conexionesCreadas++;
          } catch (error) {
            console.warn(`Error al crear arista corequisito: ${data.asignatura_objetivo.id} <-> ${co.id}`, error);
          }
        });
        
        return conexionesCreadas > 0;
      };
      
      // Ejecutar procesamiento según los datos disponibles
      // IMPORTANTE: Primero procesamos los prerrequisitos, luego la asignatura objetivo
      if (data.niveles_topologicos) {
        procesarNiveles();
      } else if (data.todos_prerrequisitos) {
        procesarPrerrequisitos();
      }
      
      // Ahora agregamos la asignatura objetivo
      procesarAsignaturaObjetivo();
      
      // Y finalmente las conexiones
      let conexionesCreadas = false;
      if (data.estructura_dependencias) {
        conexionesCreadas = procesarDependencias();
      } else {
        let conexionesPre = procesarConexionesDirectas();
        let conexionesCo = procesarCorequisitosDirectos();
        conexionesCreadas = conexionesPre || conexionesCo;
      }
      
      // Verificar que hay datos suficientes
      if (nodes.length === 0) {
        setError('No hay asignaturas para visualizar en el grafo');
        return;
      }
      
      if (nodes.length > 1 && !conexionesCreadas && edges.length === 0) {
        console.warn('Se visualizarán los nodos sin relaciones, pues no se pudieron crear aristas');
      }
      
      console.log(`Grafo creado con ${nodes.length} nodos y ${edges.length} aristas`);
      
      // Configuración de la visualización según el tipo de vista
      const treeOptions = {
        layout: {
          hierarchical: {
            direction: 'UD', // Up-to-Down
            sortMethod: 'directed',
            levelSeparation: 120,
            nodeSpacing: 180,
            treeSpacing: 200,
            blockShifting: true,
            edgeMinimization: true,
            parentCentralization: true
          }
        },
        physics: {
          hierarchicalRepulsion: {
            centralGravity: 0.1,
            springLength: 100,
            springConstant: 0.01,
            nodeDistance: 200,
            damping: 0.09
          },
          solver: 'hierarchicalRepulsion',
          stabilization: {
            enabled: true,
            iterations: 1000,
            updateInterval: 100,
            fit: true
          }
        },
        nodes: {
          margin: {
            top: 10,
            bottom: 10,
            left: 15,
            right: 15
          },
          widthConstraint: {
            maximum: 200
          },
          heightConstraint: {
            minimum: 50
          },
          shape: 'box',
          shapeProperties: {
            borderRadius: 6
          },
          shadow: {
            enabled: true,
            color: 'rgba(0,0,0,0.3)',
            size: 10,
            x: 5,
            y: 5
          }
        },
        edges: {
          arrows: {
            to: { enabled: true, scaleFactor: 1.2 }
          },
          color: {
            inherit: false
          },
          smooth: {
            enabled: true,
            type: 'cubicBezier',
            roundness: 0.4
          },
          width: 2,
          shadow: {
            enabled: true,
            color: 'rgba(0,0,0,0.3)',
            size: 5,
            x: 3,
            y: 3
          }
        },
        interaction: {
          navigationButtons: true,
          keyboard: true,
          hover: true,
          tooltipDelay: 300,
          zoomView: true,
          dragNodes: true,
          dragView: true
        }
      };
      
      const horizontalOptions = {
        layout: {
          hierarchical: {
            direction: 'LR', // Left-to-Right
            sortMethod: 'directed',
            levelSeparation: 150,
            nodeSpacing: 150,
            treeSpacing: 200
          }
        },
        physics: {
          hierarchicalRepulsion: {
            centralGravity: 0.0,
            springLength: 150,
            springConstant: 0.01,
            nodeDistance: 180,
            damping: 0.09
          },
          solver: 'hierarchicalRepulsion'
        },
        nodes: {
          margin: 10,
          widthConstraint: {
            maximum: 200
          }
        },
        edges: {
          smooth: true
        }
      };
      
      const viewOptions = view === 'tree' ? treeOptions : horizontalOptions;
      
      // Crear la red
      const network = new Network(
        containerRef.current,
        { nodes, edges },
        viewOptions
      );
      
      networkRef.current = network;
      
      // Enfocar el grafo
      network.once('stabilized', () => {
        network.fit({
          animation: {
            duration: 1000,
            easingFunction: 'easeInOutQuad'
          }
        });
      });
      
      // Limpiar error si todo sale bien
      setError(null);
    } catch (err) {
      console.error('Error al crear el grafo:', err);
      setError('Error al visualizar el grafo: ' + err.message);
    }
    
    return () => {
      if (networkRef.current) {
        networkRef.current.destroy();
        networkRef.current = null;
      }
    };
  }, [data, view]);
  
  const changeView = (newView) => {
    setView(newView);
  };
  
  if (!data) {
    return (
      <Card>
        <Card.Body className="text-center p-5">
          <p className="text-muted my-4">
            Selecciona una asignatura para visualizar su ruta académica.
          </p>
        </Card.Body>
      </Card>
    );
  }
  
  return (
    <Card>
      <Card.Body>
        <h3 className="section-title">Visualización de Prerrequisitos</h3>
        
        {error ? (
          <Alert variant="danger">
            {error}
          </Alert>
        ) : (
          <>
            <div className="d-flex justify-content-center mb-3">
              <ButtonGroup>
                <Button 
                  variant={view === 'tree' ? 'primary' : 'outline-primary'}
                  onClick={() => changeView('tree')}
                >
                  Vista Árbol
                </Button>
                <Button 
                  variant={view === 'horizontal' ? 'primary' : 'outline-primary'}
                  onClick={() => changeView('horizontal')}
                >
                  Vista Horizontal
                </Button>
              </ButtonGroup>
            </div>
            
            <div className="graph-container" ref={containerRef}></div>
            
            <div className="mt-3">
              <h5>Leyenda:</h5>
              <div className="d-flex flex-wrap gap-3 mt-2">
                <div className="d-flex align-items-center">
                  <div style={{ width: 20, height: 20, backgroundColor: '#e74c3c', marginRight: 8 }}></div>
                  <span>Asignatura Objetivo</span>
                </div>
                <div className="d-flex align-items-center">
                  <div style={{ width: 20, height: 20, backgroundColor: '#3498db', marginRight: 8 }}></div>
                  <span>Nivel 0 (Base)</span>
                </div>
                <div className="d-flex align-items-center">
                  <div style={{ width: 20, height: 20, backgroundColor: '#2ecc71', marginRight: 8 }}></div>
                  <span>Nivel 1</span>
                </div>
                <div className="d-flex align-items-center">
                  <div style={{ width: 20, height: 20, backgroundColor: '#f39c12', marginRight: 8 }}></div>
                  <span>Nivel 2</span>
                </div>
                <div className="d-flex align-items-center">
                  <div style={{ width: 20, height: 20, backgroundColor: '#9b59b6', marginRight: 8 }}></div>
                  <span>Nivel 3+</span>
                </div>
              </div>
              <div className="d-flex flex-wrap gap-3 mt-2">
                <div className="d-flex align-items-center">
                  <div style={{ display: 'flex', alignItems: 'center', marginRight: 8 }}>
                    <hr style={{ width: 20, height: 2, backgroundColor: '#2c3e50', border: 'none' }} />
                    <div style={{ width: 0, height: 0, borderLeft: '5px solid transparent', borderRight: '5px solid transparent', borderBottom: '8px solid #2c3e50', transform: 'rotate(90deg)' }}></div>
                  </div>
                  <span>Prerrequisito</span>
                </div>
                <div className="d-flex align-items-center">
                  <div style={{ display: 'flex', alignItems: 'center', marginRight: 8 }}>
                    <hr style={{ width: 20, height: 2, borderTop: '2px dashed #3498db', backgroundColor: 'transparent' }} />
                  </div>
                  <span>Corequisito</span>
                </div>
              </div>
            </div>
            
            <div className="mt-3">
              <p className="text-muted small">
                <strong>Nota:</strong> Puede arrastrar los nodos, hacer zoom con la rueda del ratón y mover el grafo completo manteniendo clic + arrastre.
              </p>
            </div>
          </>
        )}
      </Card.Body>
    </Card>
  );
};

export default GraphVisualization;