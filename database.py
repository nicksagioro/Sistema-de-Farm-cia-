"""
database.py - Configuracao do banco de dados e sessao SQLAlchemy.

Exporta:
    engine, SessionLocal, Base, get_db, init_db
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/farmacia_db"
)

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependencia FastAPI: abre e fecha a sessao por requisicao."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Cria todas as tabelas a partir dos modelos importados."""
    # A importacao aqui garante que os modelos sejam registrados no Base
    # antes de create_all ser chamado.
    from models import Base  # noqa: F401
    Base.metadata.create_all(bind=engine)
