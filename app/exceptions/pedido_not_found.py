class PedidoNotFoundError(Exception):
    def __init__(self, pedido_id: int):
        self.pedido_id = pedido_id
        super().__init__(f"Pedido com ID {pedido_id} não encontrado")