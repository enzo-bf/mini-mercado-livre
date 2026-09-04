from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


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

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, nome: str) -> str:
        nome_normalizado = nome.strip()

        if len(nome_normalizado) < 3:
            raise ValueError("Nome deve possuir ao menos 3 caracteres")

        return nome_normalizado


class AtualizarProdutoRequest(CriarProdutoRequest):
    pass


class ProdutoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    preco: Decimal
    estoque: int