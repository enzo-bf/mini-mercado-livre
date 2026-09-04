import pytest


def criar_produto(
    client,
    nome="Notebook Gamer",
    preco=5500.00,
    estoque=10
):
    response = client.post(
        "/produtos/",
        json={
            "nome": nome,
            "preco": preco,
            "estoque": estoque
        }
    )

    assert response.status_code in (200, 201)

    return response.json()


def test_criar_pedido_com_sucesso(client):
    produto = criar_produto(client)

    response = client.post(
        "/pedidos/",
        json={
            "produto_id": produto["id"],
            "quantidade": 2
        }
    )

    assert response.status_code == 201

    pedido = response.json()

    assert pedido["id"] == 1
    assert pedido["produto_id"] == produto["id"]
    assert pedido["quantidade"] == 2
    assert float(pedido["valor_total"]) == 11000.00


def test_criar_pedido_reduz_estoque(client):
    produto = criar_produto(
        client,
        estoque=10
    )

    response_pedido = client.post(
        "/pedidos/",
        json={
            "produto_id": produto["id"],
            "quantidade": 3
        }
    )

    assert response_pedido.status_code == 201

    response_produto = client.get(
        f"/produtos/{produto['id']}"
    )

    assert response_produto.status_code == 200
    assert response_produto.json()["estoque"] == 7


def test_rejeitar_pedido_com_estoque_insuficiente(client):
    produto = criar_produto(
        client,
        estoque=2
    )

    response = client.post(
        "/pedidos/",
        json={
            "produto_id": produto["id"],
            "quantidade": 5
        }
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": (
            f"Estoque insuficiente para o produto {produto['id']}. "
            "Disponível: 2. "
            "Solicitado: 5."
        )
    }


def test_estoque_nao_muda_quando_pedido_falha(client):
    produto = criar_produto(
        client,
        estoque=2
    )

    response_pedido = client.post(
        "/pedidos/",
        json={
            "produto_id": produto["id"],
            "quantidade": 5
        }
    )

    assert response_pedido.status_code == 409

    response_produto = client.get(
        f"/produtos/{produto['id']}"
    )

    assert response_produto.status_code == 200
    assert response_produto.json()["estoque"] == 2


def test_rejeitar_pedido_para_produto_inexistente(client):
    response = client.post(
        "/pedidos/",
        json={
            "produto_id": 999,
            "quantidade": 1
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Produto com ID 999 não encontrado"
    }


def test_listar_pedidos(client):
    produto = criar_produto(client)

    response_criacao = client.post(
        "/pedidos/",
        json={
            "produto_id": produto["id"],
            "quantidade": 2
        }
    )

    assert response_criacao.status_code == 201

    response = client.get("/pedidos/")

    assert response.status_code == 200

    pedidos = response.json()

    assert len(pedidos) == 1
    assert pedidos[0]["produto_id"] == produto["id"]
    assert pedidos[0]["quantidade"] == 2


def test_pedido_pode_consumir_todo_estoque(
    client,
    produto_criado
):
    estoque = produto_criado["estoque"]

    response = client.post(
        "/pedidos/",
        json={
            "produto_id": produto_criado["id"],
            "quantidade": estoque
        }
    )

    assert response.status_code == 201

    response_produto = client.get(
        f"/produtos/{produto_criado['id']}"
    )

    assert response_produto.status_code == 200
    assert response_produto.json()["estoque"] == 0


@pytest.mark.parametrize(
    "quantidade",
    [0, -1, -10]
)
def test_rejeitar_pedido_com_quantidade_invalida(
    client,
    produto_criado,
    quantidade
):
    response = client.post(
        "/pedidos/",
        json={
            "produto_id": produto_criado["id"],
            "quantidade": quantidade
        }
    )

    assert response.status_code == 422


def test_pedido_nao_e_criado_com_estoque_insuficiente(
    client,
    produto_criado
):
    response = client.post(
        "/pedidos/",
        json={
            "produto_id": produto_criado["id"],
            "quantidade": produto_criado["estoque"] + 1
        }
    )

    assert response.status_code == 409

    response_pedidos = client.get("/pedidos/")

    assert response_pedidos.status_code == 200
    assert response_pedidos.json() == []