import unittest                     
from unittest.mock import Mock, patch  
from flask import Flask            

from src.api.routes import bp       



class DummyTx:# Classe simples que simula uma transação real, serve apenas para fornecer dados de teste em um formato compatível com o que a API espera.
    def __init__(self, id, tipo, descricao, valor):
        self.id = id
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor

    def to_dict(self):# A API retorna transações como dicionários.
        return {"id": self.id, "tipo": self.tipo, "descricao": self.descricao, "valor": self.valor}# Esse método garante que possamos converter nossa versão "dummy" nesse formato esperado.


class ApiTestCase(unittest.TestCase):# Classe de testes principal, cada método test_... é um caso de teste isolado que valida o comportamento de uma rota específica.
    def setUp(self):
        # Cria uma instância do Flask apenas para rodar os testes.
        # Não precisamos do servidor rodando em localhost, tudo acontece em memória.
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True  # Ativa o modo de teste do Flask (trata erros de forma mais previsível).
        self.app.register_blueprint(bp)    # Registra o Blueprint da API sob teste.
        self.client = self.app.test_client()  # Cliente HTTP fake para enviar requisições à API.

        # Criamos um objeto "fake_manager" que simula o FinanceManager real.
        # Assim, testamos só as regras de negócio da API, sem depender de arquivos ou banco de dados.
        self.fake_manager = Mock()
        self.fake_manager.listar_transacoes.return_value = [DummyTx(1, "entrada", "Inicial", 100.0)]
        self.fake_manager.adicionar_transacao.return_value = DummyTx(2, "entrada", "Test", 100.0)
        self.fake_manager.remover_transacao.return_value = True
        self.fake_manager.calcular_saldo.return_value = 100.0

        # Patch substitui a função _manager do módulo routes.
        # Sempre que o código da API tentar criar um FinanceManager real,
        # devolvemos o nosso fake_manager configurado acima.
        self.p_manager = patch("src.api.routes._manager", return_value=self.fake_manager)
        self.p_manager.start()

    def tearDown(self):
        # Para o patch e devolve o comportamento original,
        # garantindo que outros testes não sejam impactados.
        self.p_manager.stop()

    def test_list_transactions(self):
        resp = self.client.get("/transactions")# Envia um GET para a rota /transactions
        self.assertEqual(resp.status_code, 200)  # Esperamos sucesso (200 OK).
        
        self.assertEqual(resp.get_json(), [ 
            {"id": 1, "tipo": "entrada", "descricao": "Inicial", "valor": 100.0}
        ])# A API deve retornar a lista de transações no formato JSON.
        self.fake_manager.listar_transacoes.assert_called_once()# Confirma que o método listar_transacoes foi de fato chamado.

    def test_create_transaction_ok(self):
        payload = {"tipo": "entrada", "descricao": "Test", "valor": 100.0}# Envia uma requisição POST com dados válidos.
        resp = self.client.post("/transactions", json=payload)
        self.assertEqual(resp.status_code, 201)  # Esperamos criação (201 Created).
        data = resp.get_json()
        
        # Conferimos se os dados retornados batem com o que enviamos.
        self.assertEqual(data["descricao"], "Test")
        self.assertEqual(data["valor"], 100.0)
       
        # Garante que a API chamou o método certo do manager com os argumentos corretos.
        self.fake_manager.adicionar_transacao.assert_called_once_with("entrada", "Test", 100.0)

    def test_create_transaction_missing_fields(self):
        
        payload = {"descricao": "Sem tipo", "valor": 10}# Faltando campo obrigatório "tipo".
        resp = self.client.post("/transactions", json=payload)
        self.assertEqual(resp.status_code, 400)  # A API deve recusar com erro 400 (Bad Request).
        self.assertIn("Campos obrigatórios ausentes", resp.get_json()["error"])
        self.fake_manager.adicionar_transacao.assert_not_called()# O manager não deve ser chamado em caso de erro de validação.

    def test_create_transaction_invalid_value(self):
        payload = {"tipo": "entrada", "descricao": "X", "valor": "abc"}# Campo "valor" não é numérico.
        resp = self.client.post("/transactions", json=payload)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["error"], "Valor deve ser numérico")
        self.fake_manager.adicionar_transacao.assert_not_called()

    def test_create_transaction_invalid_tipo(self):
        payload = {"tipo": "qualquer", "descricao": "X", "valor": 10}# Tipo inválido (só aceitamos "entrada" ou "saida").
        resp = self.client.post("/transactions", json=payload)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["error"], "Tipo deve ser 'entrada' ou 'saida'")
        self.fake_manager.adicionar_transacao.assert_not_called()

    def test_delete_transaction_ok(self):
        # Remoção de uma transação existente.
        resp = self.client.delete("/transactions/1")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()["ok"])  # API deve confirmar com ok=True.
        self.fake_manager.remover_transacao.assert_called_once_with(1)

    def test_delete_transaction_not_found(self):
        self.fake_manager.remover_transacao.return_value = False # Simula o caso em que a transação não existe.
        resp = self.client.delete("/transactions/999")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.get_json()["error"], "Transação não encontrada")
        self.fake_manager.remover_transacao.assert_called_with(999)

    def test_get_balance(self):
        self.fake_manager.calcular_saldo.return_value = 42.5 # Força o saldo para um valor conhecido. 
        resp = self.client.get("/balance")
        self.assertEqual(resp.status_code, 200)
        # Verifica se a resposta da API contém o saldo configurado.
        self.assertEqual(resp.get_json()["balance"], 42.5)
        self.fake_manager.calcular_saldo.assert_called_once()

    def test_update_transaction_ok(self):# Testa a atualização bem-sucedida de uma transação existente.
        payload = {"tipo": "saida", "descricao": "Novo tipo", "valor": 150.0}
        self.fake_manager.atualizar_transacao.return_value = DummyTx(1, "saida", "Novo tipo", 150.0)  # Simula a transação atualizada.
        
        resp = self.client.put("/transactions/1", json=payload)
        self.assertEqual(resp.status_code, 200)  # Espera o status de sucesso (200 OK).
        
        # Verifica se a transação foi realmente atualizada.
        data = resp.get_json()
        self.assertEqual(data["descricao"], "Novo tipo")
        self.assertEqual(data["valor"], 150.0)
        
        
        self.fake_manager.atualizar_transacao.assert_called_once_with(1, "saida", "Novo tipo", 150.0)# Garante que o método de atualização foi chamado com os parâmetros corretos.

    def test_update_transaction_not_found(self):# Testa o caso de tentativa de atualização de uma transação inexistente.
        payload = {"tipo": "saida", "descricao": "Novo tipo", "valor": 150.0}
        self.fake_manager.atualizar_transacao.return_value = None  # Simula que a transação não foi encontrada.
        
        resp = self.client.put("/transactions/999", json=payload)
        self.assertEqual(resp.status_code, 404)  # Espera o status de erro (404 Not Found).
        self.assertEqual(resp.get_json()["error"], "Transação não encontrada")
        
        
        self.fake_manager.atualizar_transacao.assert_called_once_with(999, "saida", "Novo tipo", 150.0)# Garante que o método de atualização foi chamado com o ID correto.

    def test_update_transaction_missing_fields(self):# Testa o caso em que faltam campos obrigatórios.
        payload = {"descricao": "Faltando tipo", "valor": 100.0}  # Faltando o campo "tipo".
        resp = self.client.put("/transactions/1", json=payload)
        self.assertEqual(resp.status_code, 400)  # Espera o erro (400 Bad Request).
        self.assertIn("Campos obrigatórios ausentes", resp.get_json()["error"])
        
        
        self.fake_manager.atualizar_transacao.assert_not_called()# Garante que o método de atualização não foi chamado se os dados estiverem incompletos.

    def test_update_transaction_invalid_value(self):# Testa o caso em que o valor não é numérico.
        payload = {"tipo": "entrada", "descricao": "Valor inválido", "valor": "abc"}  # Valor não numérico.
        resp = self.client.put("/transactions/1", json=payload)
        self.assertEqual(resp.status_code, 400)  # Espera o erro (400 Bad Request).
        self.assertEqual(resp.get_json()["error"], "Valor deve ser numérico")
        
        
        self.fake_manager.atualizar_transacao.assert_not_called()# Garante que o método de atualização não foi chamado com um valor inválido.

    def test_update_transaction_invalid_tipo(self):# Testa o caso em que o tipo não é válido.
        payload = {"tipo": "qualquer", "descricao": "Tipo inválido", "valor": 100.0}  # Tipo inválido.
        resp = self.client.put("/transactions/1", json=payload)
        self.assertEqual(resp.status_code, 400)  # Espera o erro (400 Bad Request).
        self.assertEqual(resp.get_json()["error"], "Tipo deve ser 'entrada' ou 'saida'")
        
        
        self.fake_manager.atualizar_transacao.assert_not_called()# Garante que o método de atualização não foi chamado com um tipo inválido.
     

# Permite rodar este arquivo diretamente como script.
if __name__ == "__main__":
    unittest.main()
