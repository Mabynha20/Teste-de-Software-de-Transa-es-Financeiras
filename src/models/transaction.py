
from datetime import datetime

class Transaction:
    def __init__(self, id: int, tipo: str, descricao: str, valor: float, data: str = None):
        self.id = id
        self.tipo = tipo  # 'entrada' | 'saida'
        self.descricao = descricao
        self.valor = float(valor)
        self.data = data or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "valor": self.valor,
            "data": self.data,
        }

    @staticmethod
    def from_dict(d: dict):
        return Transaction(
            id=d["id"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            valor=d["valor"],
            data=d.get("data"),
        )
