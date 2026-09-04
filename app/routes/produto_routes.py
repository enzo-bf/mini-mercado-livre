from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.produto_schema import (
    AtualizarProdutoRequest,
    CriarProdutoRequest,
    ProdutoResponse
)
from app.services.produto_service import ProdutoService

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

service = ProdutoService()


@router.post(
    "/",
    response_model=ProdutoResponse
)
def criar_produto(
    request: CriarProdutoRequest,
    db: Session = Depends(get_db)
):

    return service.criar_produto(
        db,
        request
    )


@router.get(
    "/",
    response_model=list[ProdutoResponse]
)
def listar_produtos(
    db: Session = Depends(get_db)
):

    return service.listar_produtos(db)


@router.get(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):

    return service.buscar_por_id(
        db,
        produto_id
    )


@router.put(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def atualizar_produto(
    produto_id: int,
    request: AtualizarProdutoRequest,
    db: Session = Depends(get_db)
):
    return service.atualizar_produto(
        db,
        produto_id,
        request
    )


@router.delete(
    "/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    service.excluir_produto(db, produto_id)