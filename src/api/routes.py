
from flask import Blueprint, request, jsonify, current_app
from src.services.finance_manager import FinanceManager

bp = Blueprint("api", __name__)

def _manager():
    storage_file = current_app.config.get("STORAGE_FILE")
    return FinanceManager(storage_file=storage_file)

@bp.get("/transactions")
def list_transactions():
    fm = _manager()
    data = [t.to_dict() for t in fm.listar_transacoes()]
    return jsonify(data), 200

@bp.post("/transactions")
def create_transaction():
    fm = _manager()
    payload = request.get_json(silent=True) or {}

    missing = [k for k in ("tipo", "descricao", "valor") if k not in payload]
    if missing:
        return jsonify(error=f"Campos obrigatórios ausentes: {', '.join(missing)}"), 400

    try:
        valor = float(payload["valor"])
    except (TypeError, ValueError):
        return jsonify(error="Valor deve ser numérico"), 400

    if payload["tipo"] not in ("entrada", "saida"):
        return jsonify(error="Tipo deve ser 'entrada' ou 'saida'"), 400

    t = fm.adicionar_transacao(payload["tipo"], payload["descricao"], valor)
    return jsonify(t.to_dict()), 201

@bp.delete("/transactions/<int:tid>")
def delete_transaction(tid: int):
    fm = _manager()
    ok = fm.remover_transacao(tid)
    if not ok:
        return jsonify(error="Transação não encontrada"), 404
    return jsonify(ok=True), 200

@bp.get("/balance")
def get_balance():
    fm = _manager()
    return jsonify(balance=fm.calcular_saldo()), 200

@bp.put("/transactions/<int:tid>")
def put_transaction(tid: int):
    fm = _manager()
    payload = request.get_json(silent=True) or {}

    missing = [k for k in ("tipo", "descricao", "valor") if k not in payload]
    if missing:
        return jsonify(error=f"Campos obrigatórios ausentes: {', '.join(missing)}"), 400

    try:
        valor = float(payload["valor"])
    except (TypeError, ValueError):
        return jsonify(error="Valor deve ser numérico"), 400

    if payload["tipo"] not in ("entrada", "saida"):
        return jsonify(error="Tipo deve ser 'entrada' ou 'saida'"), 400

    transacao_atualizada = fm.atualizar_transacao(tid, payload["tipo"], payload["descricao"], valor)
    if not transacao_atualizada:
        return jsonify(error="Transação não encontrada"), 404

    return jsonify(transacao_atualizada.to_dict()), 200
