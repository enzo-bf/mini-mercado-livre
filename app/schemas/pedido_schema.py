from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CriarPedidoRequest(BaseModel):
    produto_id: int = Field(
        gt=0,
        examples=[1]
    )

    quantidade: int = Field(
        gt=0,
        examples=[2]
    )


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    produto_id: int
    quantidade: int
    valor_total: Decimal