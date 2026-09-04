from sqlalchemy.orm import Session

from app.models.pedido import Pedido


class PedidoRepository:

    def criar(
        self,
        db: Session,
        pedido: Pedido
    ) -> Pedido:
        db.add(pedido)
        db.flush()

        return pedido

    def listar(
        self,
        db: Session
    ) -> list[Pedido]:
        return db.query(Pedido).all()

    def buscar_por_id(
        self,
        db: Session,
        pedido_id: int
    ) -> Pedido | None:
        return (
            db.query(Pedido)
            .filter(Pedido.id == pedido_id)
            .first()
        )

    def existe_por_produto_id(
        self,
        db: Session,
        produto_id: int
    ) -> bool:
        return (
            db.query(Pedido.id)
            .filter(Pedido.produto_id == produto_id)
            .first()
            is not None
        )