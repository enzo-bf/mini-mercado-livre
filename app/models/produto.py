from decimal import Decimal

from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class Produto(Base):

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    preco: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    estoque: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
