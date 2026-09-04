class EstoqueInsuficienteError(Exception):
    def __init__(
        self,
        produto_id: int,
        estoque_disponivel: int,
        quantidade_solicitada: int
    ):
        self.produto_id = produto_id
        self.estoque_disponivel = estoque_disponivel
        self.quantidade_solicitada = quantidade_solicitada

        mensagem = (
            f"Estoque insuficiente para o produto {produto_id}. "
            f"Disponível: {estoque_disponivel}. "
            f"Solicitado: {quantidade_solicitada}."
        )

        super().__init__(mensagem)