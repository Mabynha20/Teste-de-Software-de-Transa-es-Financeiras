
import json
import os
from typing import List
from src.models.transaction import Transaction

class FileStorage:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load(self) -> List[Transaction]:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Transaction.from_dict(d) for d in data]

    def save(self, transacoes: List[Transaction]):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in transacoes], f, indent=2, ensure_ascii=False)
