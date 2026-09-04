from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CriarProdutoRequest(BaseModel):
    nome: str = Field(
        min_length=3,
        max_length=100,
        examples=["Notebook Gamer"]
    )
    preco: Decimal = Field(
        gt=0,
        decimal_places=2,
        examples=[5500.00]
    )
    estoque: int = Field(
        ge=0,
        examples=[10]
    )


class ProdutoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    preco: Decimal
    estoque: int