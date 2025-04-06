/**
 * Configuración global de la aplicación
 */

const config = {
    // API
    api: {
      baseUrl: 'http://127.0.0.1:8000/api/v1',
      timeout: 30000, // 30 segundos
    },
    
    // Grafo
    graph: {
      // Colores para los diferentes niveles
      levelColors: [
        '#3498db', // Azul - Nivel 0
        '#2ecc71', // Verde - Nivel 1
        '#f39c12', // Naranja - Nivel 2
        '#9b59b6', // Púrpura - Nivel 3
        '#e74c3c', // Rojo - Nivel 4
        '#1abc9c', // Turquesa - Nivel 5
        '#d35400', // Naranja oscuro - Nivel 6
        '#8e44ad', // Púrpura oscuro - Nivel 7
      ],
      
      // Color para la asignatura objetivo
      targetColor: '#e74c3c',
      
      // Dimensiones del contenedor del grafo
      containerHeight: '600px',
      
      // Opciones para la visualización jerárquica
      hierarchical: {
        direction: 'LR',
        levelSeparation: 150,
        nodeSpacing: 150,
      },
      
      // Opciones para la visualización radial
      radial: {
        springLength: 150,
        springConstant: 0.08,
        gravitationalConstant: -100,
      },
    },
    
    // Aplicación
    app: {
      name: 'RutaAcadémica',
      description: 'Sistema de Análisis de Prerrequisitos Académicos',
      version: '1.0.0',
      footer: `© ${new Date().getFullYear()} RutaAcadémica - Todos los derechos reservados`,
    },
    
    // Opciones de visualización
    ui: {
      theme: {
        primary: '#3498db',
        secondary: '#2ecc71',
        accent: '#f39c12',
        danger: '#e74c3c',
        dark: '#2c3e50',
        light: '#ecf0f1',
      },
      animations: true,
      showTooltips: true,
    },
  };
  
  export default config;