from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database.base import Base
from app.database.connection import engine
from app.exceptions.produto_associado_pedido import (
    ProdutoAssociadoPedidoError
)
from app.exceptions.pedido_not_found import PedidoNotFoundError
from app.exceptions.produto_not_found import ProdutoNotFoundError
from app.routes.health_routes import router as health_router
from app.routes.pedido_routes import router as pedido_router
from app.routes.produto_routes import router as produto_router

from app.exceptions.estoque_insuficiente import (
    EstoqueInsuficienteError
)
from app.models import Pedido, Produto

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Mercado Livre",
    version="1.0.0",
    description="API para estudos de arquitetura Back-End"
)

app.include_router(health_router)
app.include_router(produto_router)
app.include_router(pedido_router)

@app.exception_handler(EstoqueInsuficienteError)
def estoque_insuficiente_handler(
    request: Request,
    exception: EstoqueInsuficienteError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exception)
        }
    )

@app.exception_handler(ProdutoNotFoundError)
def produto_not_found_handler(
    request: Request,
    exception: ProdutoNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exception)
        }
    )


@app.exception_handler(PedidoNotFoundError)
def pedido_not_found_handler(
    request: Request,
    exception: PedidoNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exception)
        }
    )


@app.exception_handler(ProdutoAssociadoPedidoError)
def produto_associado_pedido_handler(
    request: Request,
    exception: ProdutoAssociadoPedidoError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exception)
        }
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
