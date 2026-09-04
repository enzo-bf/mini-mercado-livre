from sqlalchemy.orm import Session

from app.models.produto import Produto


class ProdutoRepository:

    def criar(
        self,
        db: Session,
        produto: Produto
    ) -> Produto:

        db.add(produto)
        db.commit()
        db.refresh(produto)

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