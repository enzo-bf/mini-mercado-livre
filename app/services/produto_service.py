from sqlalchemy.orm import Session

from app.exceptions.produto_not_found import ProdutoNotFoundError
from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.produto_schema import CriarProdutoRequest


class ProdutoService:
    def __init__(self):
        self.repository = ProdutoRepository()

    def criar_produto(
        self,
        db: Session,
        request: CriarProdutoRequest
    ) -> Produto:
        produto = Produto(
            nome=request.nome.strip(),
            preco=request.preco,
            estoque=request.estoque
        )

        return self.repository.criar(db, produto)

    def listar_produtos(
        self,
        db: Session
    ) -> list:
        return self.repository.listar(db)

    def buscar_por_id(
        self,
        db: Session,
        produto_id: int
    ) -> Produto:
        produto = self.repository.buscar_por_id(db, produto_id)

        if produto is None:
            raise ProdutoNotFoundError(produto_id)

        return produto