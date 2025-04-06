import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base import Base
from app.models import asignatura, carrera, pensum, trimestre


def init_db():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente")


if __name__ == "__main__":
    init_db()
