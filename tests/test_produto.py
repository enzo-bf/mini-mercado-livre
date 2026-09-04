import pytest

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


def test_atualizar_produto_com_sucesso(client, produto_criado):
    response = client.put(
        f"/produtos/{produto_criado['id']}",
        json={
            "nome": "Notebook Profissional",
            "preco": 6200.00,
            "estoque": 15
        }
    )

    assert response.status_code == 200
    assert response.json()["nome"] == "Notebook Profissional"
    assert float(response.json()["preco"]) == 6200.00
    assert response.json()["estoque"] == 15


def test_atualizar_produto_inexistente(client):
    response = client.put(
        "/produtos/999",
        json={
            "nome": "Notebook Profissional",
            "preco": 6200.00,
            "estoque": 15
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Produto com ID 999 não encontrado"
    }


def test_atualizar_produto_com_dados_invalidos(client, produto_criado):
    response = client.put(
        f"/produtos/{produto_criado['id']}",
        json={
            "nome": "AB",
            "preco": 0,
            "estoque": -1
        }
    )

    assert response.status_code == 422

    produto = client.get(
        f"/produtos/{produto_criado['id']}"
    ).json()
    assert produto["nome"] == produto_criado["nome"]
    assert float(produto["preco"]) == float(produto_criado["preco"])
    assert produto["estoque"] == produto_criado["estoque"]


def test_excluir_produto_com_sucesso(client, produto_criado):
    response = client.delete(
        f"/produtos/{produto_criado['id']}"
    )

    assert response.status_code == 204
    assert response.content == b""

    busca = client.get(
        f"/produtos/{produto_criado['id']}"
    )
    assert busca.status_code == 404


def test_excluir_produto_inexistente(client):
    response = client.delete("/produtos/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Produto com ID 999 não encontrado"
    }


def test_nao_excluir_produto_associado_a_pedido(client, produto_criado):
    pedido = client.post(
        "/pedidos/",
        json={
            "produto_id": produto_criado["id"],
            "quantidade": 1
        }
    )
    assert pedido.status_code == 201

    response = client.delete(
        f"/produtos/{produto_criado['id']}"
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": (
            f"Produto com ID {produto_criado['id']} está associado a pedidos"
        )
    }

    produto = client.get(
        f"/produtos/{produto_criado['id']}"
    )
    assert produto.status_code == 200

    pedidos = client.get("/pedidos/")
    assert pedidos.status_code == 200
    assert len(pedidos.json()) == 1
    assert pedidos.json()[0]["id"] == pedido.json()["id"]