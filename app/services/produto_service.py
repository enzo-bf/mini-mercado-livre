from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.produto_associado_pedido import (
    ProdutoAssociadoPedidoError
)
from app.exceptions.produto_not_found import ProdutoNotFoundError
from app.models.produto import Produto
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.produto_schema import (
    AtualizarProdutoRequest,
    CriarProdutoRequest
)


class ProdutoService:
    def __init__(self):
        self.repository = ProdutoRepository()
        self.pedido_repository = PedidoRepository()

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

    def atualizar_produto(
        self,
        db: Session,
        produto_id: int,
        request: AtualizarProdutoRequest
    ) -> Produto:
        produto = self.buscar_por_id(db, produto_id)

        produto.nome = request.nome.strip()
        produto.preco = request.preco
        produto.estoque = request.estoque

        return self.repository.atualizar(db, produto)

    def excluir_produto(
        self,
        db: Session,
        produto_id: int
    ) -> None:
        produto = self.buscar_por_id(db, produto_id)

        if self.pedido_repository.existe_por_produto_id(db, produto_id):
            raise ProdutoAssociadoPedidoError(produto_id)

        try:
            self.repository.excluir(db, produto)
        except IntegrityError:
            db.rollback()
            raise ProdutoAssociadoPedidoError(produto_id)