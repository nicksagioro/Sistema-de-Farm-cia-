"""
test_conftest.py - Configuracao compartilhada dos testes.

Importado automaticamente pelo pytest via conftest.py.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import get_db
from models import Base
from app import app

_engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
)


@event.listens_for(_engine, "connect")
def _fk_pragma(dbapi_conn, _):
    dbapi_conn.cursor().execute("PRAGMA foreign_keys=ON")


_Session = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
Base.metadata.create_all(bind=_engine)


def _get_db_override():
    db = _Session()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _get_db_override
client = TestClient(app)
