
import os
from typing import List, Optional
from src.models.transaction import Transaction
from src.storage.file_storage import FileStorage

class FinanceManager:
    def __init__(self, storage_file: Optional[str] = None):
        storage_path = storage_file or os.getenv("STORAGE_FILE", "./data/transacoes.json")
        self.storage = FileStorage(storage_path)
        self.transacoes: List[Transaction] = self.storage.load()

    def _persist(self):
        self.storage.save(self.transacoes)

    def _next_id(self) -> int:
        return (max([t.id for t in self.transacoes], default=0) + 1) if self.transacoes else 1

    def adicionar_transacao(self, tipo: str, descricao: str, valor: float) -> Transaction:
        t = Transaction(id=self._next_id(), tipo=tipo, descricao=descricao, valor=valor)
        self.transacoes.append(t)
        self._persist()
        return t

    def listar_transacoes(self) -> List[Transaction]:
        return list(self.transacoes)

    def remover_transacao(self, tid: int) -> bool:
        before = len(self.transacoes)
        self.transacoes = [t for t in self.transacoes if t.id != tid]
        removed = len(self.transacoes) != before
        if removed:
            self._persist()
        return removed

    def calcular_saldo(self) -> float:
        saldo = 0.0
        for t in self.transacoes:
            if t.tipo == "entrada":
                saldo += t.valor
            elif t.tipo == "saida":
                saldo -= t.valor
        return round(saldo, 2)

    def atualizar_transacao(self, tid: int, tipo: Optional[str] = None, descricao: Optional[str] = None, valor: Optional[float] = None) -> Optional[Transaction]:
        transacao = next((t for t in self.transacoes if t.id == tid), None)
        if not transacao:
            return None  
        if tipo is not None:
            transacao.tipo = tipo
        if descricao is not None:
            transacao.descricao = descricao
        if valor is not None:
            transacao.valor = valor
        self._persist()
        return transacao  
