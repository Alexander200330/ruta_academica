# RutaAcadémica: Sistema de Análisis de Prerrequisitos Académicos

Este proyecto implementa un sistema llamado "RutaAcadémica" que utiliza grafos dirigidos para identificar todas las asignaturas previas necesarias para cursar una materia específica en diferentes planes de estudio universitarios.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Alexander200330/ruta_academica.git
   cd ruta_academica_intec
   ```

2. Crea y activa un entorno virtual:

   ### Windows
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   ### macOS/Linux
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración de la base de datos

1. Crea las tablas de la base de datos:
   ```bash
   python scripts/create_db.py
   ```

2. Carga los datos de muestra:
   ```bash
   python scripts/import_data.py
   ```

## Iniciar la aplicación

Para iniciar el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en [http://localhost:8000](http://localhost:8000). La documentación interactiva de la API estará disponible en [http://localhost:8000/docs](http://localhost:8000/docs).

## Estructura del proyecto

```
ruta_academica/
│
├── app/                           # Código fuente principal
│   ├── api/                       # Definición de la API
│   ├── core/                      # Funcionalidad central y configuraciones
│   ├── db/                        # Capa de acceso a datos
│   ├── models/                    # Modelos SQLAlchemy
│   ├── schemas/                   # Esquemas Pydantic
│   └── services/                  # Servicios de negocio
│
├── scripts/                       # Scripts utilitarios
│   ├── create_db.py               # Script para crear/inicializar la base de datos
│   └── import_data.py             # Script para importar datos iniciales
│
└── requirements.txt               # Dependencias del proyecto
```

## Tecnologías utilizadas

- FastAPI: Framework web para construcción de APIs
- SQLAlchemy: ORM para interacción con bases de datos
- Pydantic: Validación de datos
- NetworkX: Biblioteca para manipulación de grafos
- Uvicorn: Servidor ASGI para Python

## Solución de problemas

Si encuentras problemas durante la instalación o ejecución:

1. Verifica que tu versión de Python sea compatible (3.8+)
2. Asegúrate de que el entorno virtual esté activo
3. Verifica que todas las dependencias estén instaladas correctamente

Para errores específicos, consulta los mensajes de error en la consola o en los logs.