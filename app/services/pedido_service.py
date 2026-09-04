from sqlalchemy.orm import Session

from app.exceptions.estoque_insuficiente import (
    EstoqueInsuficienteError
)
from app.exceptions.produto_not_found import (
    ProdutoNotFoundError
)
from app.models.pedido import Pedido
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.pedido_schema import CriarPedidoRequest


class PedidoService:

    def __init__(self):
        self.pedido_repository = PedidoRepository()
        self.produto_repository = ProdutoRepository()

    def criar_pedido(
        self,
        db: Session,
        request: CriarPedidoRequest
    ) -> Pedido:
        produto = self.produto_repository.buscar_por_id(
            db,
            request.produto_id
        )

        if produto is None:
            raise ProdutoNotFoundError(request.produto_id)

        if produto.estoque < request.quantidade:
            raise EstoqueInsuficienteError(
                produto_id=produto.id,
                estoque_disponivel=produto.estoque,
                quantidade_solicitada=request.quantidade
            )

        valor_total = produto.preco * request.quantidade

        pedido = Pedido(
            produto_id=produto.id,
            quantidade=request.quantidade,
            valor_total=valor_total
        )

        try:
            produto.estoque -= request.quantidade

            pedido_criado = self.pedido_repository.criar(
                db,
                pedido
            )

            db.commit()
            db.refresh(pedido_criado)

            return pedido_criado

        except Exception:
            db.rollback()
            raise

    def listar_pedidos(
        self,
        db: Session
    ) -> list[Pedido]:
        return self.pedido_repository.listar(db)

    def buscar_por_id(
        self,
        db: Session,
        pedido_id: int
    ) -> Pedido | None:
        return self.pedido_repository.buscar_por_id(
            db,
            pedido_id
        )