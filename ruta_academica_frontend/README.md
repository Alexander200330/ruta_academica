# RutaAcadémica - Frontend

Frontend para el sistema de análisis de prerrequisitos académicos mediante grafos dirigidos.

## Características

- Visualización interactiva de grafos de prerrequisitos académicos
- Selección de carreras, pensums y asignaturas
- Múltiples vistas de visualización (jerárquica y radial)
- Información detallada sobre asignaturas y sus dependencias
- Detección y visualización de ciclos en los prerrequisitos
- Interfaz responsiva y amigable

## Requisitos

- Node.js 14.x o superior
- npm 6.x o superior
- Backend de RutaAcadémica (API) ejecutándose en localhost:8000

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Alexander200330/ruta_academica.git
   cd ruta-academica-frontend
   ```

2. Instalar las dependencias:
   ```bash
   npm install
   ```

3. Configurar la conexión con el backend:
   - Editar `src/config.js` y cambiar la URL base de la API si es necesario

4. Iniciar la aplicación en modo desarrollo:
   ```bash
   npm start
   ```

La aplicación estará disponible en [http://localhost:3000](http://localhost:3000).

## Estructura del proyecto

```
ruta_academica_frontend/
├── public/                  # Archivos públicos
│   └── index.html           # HTML principal
├── src/                     # Código fuente
│   ├── assets/              # Imágenes y recursos estáticos
│   ├── components/          # Componentes React reutilizables
│   │   ├── AsignaturaInfo.jsx     # Información de asignatura
│   │   ├── AsignaturaInput.jsx    # Búsqueda de asignaturas
│   │   ├── CarreraSelector.jsx    # Selector de carreras
│   │   ├── Footer.jsx             # Pie de página
│   │   ├── GraphVisualization.jsx # Visualización de grafos
│   │   ├── Navbar.jsx             # Barra de navegación
│   │   ├── PensumSelector.jsx     # Selector de pensums
│   │   └── ProgressTracker.jsx    # Tracker de progreso
│   ├── pages/               # Páginas de la aplicación
│   │   ├── About.jsx              # Página "Acerca de"
│   │   ├── Home.jsx               # Página de inicio
│   │   └── RutaAcademica.jsx      # Página principal
│   ├── services/            # Servicios (API, etc.)
│   │   └── api.js                 # Cliente API
│   ├── utils/               # Utilidades
│   │   ├── dataAdapter.js         # Adaptador de datos API
│   │   └── graphUtils.js          # Utilidades para grafos
│   ├── App.jsx              # Componente principal
│   ├── config.js            # Configuración global
│   ├── index.js             # Punto de entrada
│   └── styles.css           # Estilos globales
└── package.json             # Dependencias y scripts
```

## Tecnologías utilizadas

- React 18
- React Bootstrap
- vis.js (visualización de grafos)
- React Router
- Axios (cliente HTTP)
- React Toastify (notificaciones)

## API

El frontend se comunica con el backend a través de los siguientes endpoints:

- `GET /api/v1/carreras/` - Obtener todas las carreras
- `GET /api/v1/pensums/by-carrera/{carrera_id}` - Obtener pensums de una carrera
- `GET /api/v1/asignaturas/by-pensum/{pensum_id}` - Obtener asignaturas de un pensum
- `GET /api/v1/prerrequisitos/ruta-por-codigo/{codigo}?pensum_id={id}` - Obtener ruta académica

## Personalización

Para personalizar la aplicación, puedes modificar:

- `src/config.js` - Configuración global (colores, API, opciones)
- `src/styles.css` - Estilos globales
- Componentes individuales según necesidades específicas

## Licencia

© 2023 RutaAcadémica - Todos los derechos reservados