import pytest

from tests.conftest import produto_payload

def test_criar_produto_com_sucesso(client):
    response = client.post(
        "/produtos/",
        json={
            "nome": "Notebook Gamer",
            "preco": 5500.00,
            "estoque": 10
        }
    )

    assert response.status_code == 200

    produto = response.json()

    assert produto["id"] == 1
    assert produto["nome"] == "Notebook Gamer"
    assert float(produto["preco"]) == 5500.00
    assert produto["estoque"] == 10


def test_listar_produtos(client):
    client.post(
        "/produtos/",
        json={
            "nome": "Teclado Mecânico",
            "preco": 350.00,
            "estoque": 20
        }
    )

    response = client.get("/produtos/")

    assert response.status_code == 200

    produtos = response.json()

    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Teclado Mecânico"


def test_buscar_produto_inexistente(client):
    response = client.get("/produtos/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Produto com ID 999 não encontrado"
    }


def test_rejeitar_produto_com_dados_invalidos(client):
    response = client.post(
        "/produtos/",
        json={
            "nome": "",
            "preco": -100,
            "estoque": -5
        }
    )

    assert response.status_code == 422

@pytest.mark.parametrize(
    "payload",
    [
        {
            "nome": "",
            "preco": 100,
            "estoque": 10
        },
        {
            "nome": "AB",
            "preco": 100,
            "estoque": 10
        },
        {
            "nome": "Notebook",
            "preco": 0,
            "estoque": 10
        },
        {
            "nome": "Notebook",
            "preco": -100,
            "estoque": 10
        },
        {
            "nome": "Notebook",
            "preco": 100,
            "estoque": -1
        }
    ]
)
def test_rejeitar_produto_com_dados_invalidos(
    client,
    payload
):
    response = client.post(
        "/produtos/",
        json=payload
    )

    assert response.status_code == 422

def test_criar_produto_retorna_contrato_esperado(
    client,
    produto_payload
):
    response = client.post(
        "/produtos/",
        json=produto_payload
    )

    assert response.status_code in (200, 201)

    produto = response.json()

    assert set(produto.keys()) == {
        "id",
        "nome",
        "preco",
        "estoque"
    }

    assert isinstance(produto["id"], int)
    assert produto["id"] > 0

    assert isinstance(produto["nome"], str)
    assert produto["nome"] == produto_payload["nome"]

    assert float(produto["preco"]) == produto_payload["preco"]
    assert produto["estoque"] == produto_payload["estoque"]