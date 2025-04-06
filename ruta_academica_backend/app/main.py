from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import asignaturas, carreras, pensums, trimestres, prerrequisitos
from app.core.config import settings

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(
    asignaturas.router,
    prefix=f"{settings.API_PREFIX}/asignaturas",
    tags=["asignaturas"],
)
app.include_router(
    carreras.router, prefix=f"{settings.API_PREFIX}/carreras", tags=["carreras"]
)
app.include_router(
    pensums.router, prefix=f"{settings.API_PREFIX}/pensums", tags=["pensums"]
)
app.include_router(
    trimestres.router, prefix=f"{settings.API_PREFIX}/trimestres", tags=["trimestres"]
)
app.include_router(
    prerrequisitos.router,
    prefix=f"{settings.API_PREFIX}/prerrequisitos",
    tags=["prerrequisitos"],
)


@app.get("/", tags=["root"])
async def root():
    """
    Endpoint raíz que proporciona información básica sobre la API
    """
    return {
        "app_name": "RutaAcadémica API",
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "docs_url": "/docs",
    }
