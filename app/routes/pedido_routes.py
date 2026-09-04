from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.pedido_schema import (
    CriarPedidoRequest,
    PedidoResponse
)
from app.services.pedido_service import PedidoService


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

service = PedidoService()


@router.post(
    "/",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_pedido(
    request: CriarPedidoRequest,
    db: Session = Depends(get_db)
):
    return service.criar_pedido(
        db,
        request
    )


@router.get(
    "/",
    response_model=list[PedidoResponse]
)
def listar_pedidos(
    db: Session = Depends(get_db)
):
    return service.listar_pedidos(db)


@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse
)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    return service.buscar_por_id(
        db,
        pedido_id
    )