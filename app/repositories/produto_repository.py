from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.produto import Produto


class ProdutoRepository:

    def criar(
        self,
        db: Session,
        produto: Produto
    ) -> Produto:

        db.add(produto)
        try:
            db.commit()
            db.refresh(produto)
        except SQLAlchemyError:
            db.rollback()
            raise

        return produto

    def listar(
        self,
        db: Session
    ) -> list[Produto]:

        return db.query(Produto).all()

    def buscar_por_id(
        self,
        db: Session,
        produto_id: int
    ) -> Produto | None:

        return (
            db.query(Produto)
            .filter(Produto.id == produto_id)
            .first()
        )

    def atualizar(
        self,
        db: Session,
        produto: Produto
    ) -> Produto:
        db.commit()
        db.refresh(produto)

        return produto

    def excluir(
        self,
        db: Session,
        produto: Produto
    ) -> None:
        try:
            db.delete(produto)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise