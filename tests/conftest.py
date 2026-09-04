import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.dependencies.database import get_db
from app.main import app
from app.models.pedido import Pedido
from app.models.produto import Produto


TEST_DATABASE_URL = "sqlite://"


engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)


TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)


def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def preparar_banco():
    Base.metadata.create_all(bind=engine_test)

    yield

    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
@pytest.fixture
def produto_payload():
    return {
        "nome": "Notebook Gamer",
        "preco": 5500.00,
        "estoque": 10
    }


@pytest.fixture
def produto_criado(client, produto_payload):
    response = client.post(
        "/produtos/",
        json=produto_payload
    )

    assert response.status_code in (200, 201)

    return response.json()

@pytest.fixture
def produto_payload():
    return {
        "nome": "Notebook Gamer",
        "preco": 5500.00,
        "estoque": 10
    }
