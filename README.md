# RutaAcadémica

Sistema integral para visualizar y analizar prerrequisitos académicos en planes de estudio universitarios mediante grafos.

## Estructura del proyecto

```
ruta_academica/
├── ruta_academica_backend/   # API y lógica de negocio (FastAPI, Python)
└── ruta_academica_frontend/  # Interfaz de usuario (React)
```

## Inicio rápido

### Backend

```bash
cd ruta_academica_backend
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python scripts/create_db.py
python scripts/import_data.py
uvicorn app.main:app --reload
```

API disponible en [http://localhost:8000](http://localhost:8000)

### Frontend

```bash
cd ruta_academica_frontend
npm install
npm start
```

Aplicación disponible en [http://localhost:3000](http://localhost:3000)

## Documentación detallada

- [Documentación del Backend](./ruta_academica_backend/README.md)
- [Documentación del Frontend](./ruta_academica_frontend/README.md)

## Características principales

- Visualización interactiva de grafos de prerrequisitos
- API RESTful para integración con otros sistemas
- Múltiples vistas de visualización (jerárquica y radial)
- Detección de ciclos en los prerrequisitos
- Interfaz responsiva y amigable

## Licencia
---

Desarrollado por Alexander V. y Jimmy.