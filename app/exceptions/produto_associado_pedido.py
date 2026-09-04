class ProdutoAssociadoPedidoError(Exception):
    def __init__(self, produto_id: int):
        self.produto_id = produto_id
        super().__init__(
            f"Produto com ID {produto_id} está associado a pedidos"
        )