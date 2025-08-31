import unittest
import os
import sys
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from services.finance_manager import FinanceManager
class TestFinanceManager(unittest.TestCase):

        def setUp(self):
                # Criar um arquivo temporário para os testes
                self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
                self.temp_file.write('[]')
                self.temp_file.close()

        def tearDown(self):
                # Limpar o arquivo temporário
                if os.path.exists(self.temp_file.name):
                 os.unlink(self.temp_file.name)
        
        def test_adicionar_e_listar_transacoes(self):
                fm = FinanceManager(self.temp_file.name) #Aqui foi criado uma instância chamada FinanceManager com um arquivo temporario para armazenar os valores dos futuros testes.
                
                # Adicionar uma entrada
                entrada = fm.adicionar_transacao("entrada", "Compra de alimentos", 100.0)#Aqui foi criado uma variavel para declarar os valores da entrada.
                self.assertEqual(entrada.descricao, "Compra de alimentos")#Aqui será verificado com a função (self.assertEqual) se o valor da entrada (descrição) está retornando corretamente.
                self.assertEqual(entrada.valor, 100.0)#Aqui será verificado com a função (self.assertEqual) se o valor da entrada (valor) está retornando corretamente.
                self.assertEqual(entrada.tipo, "entrada")#Aqui será verificado com a função (self.assertEqual) se o valor da entrada (tipo) está retornando corretamente.
                
                # Adicionar uma saída
                saida = fm.adicionar_transacao("saida", "Pagamento de contas", 50.0)#Aqui foi criado uma variavel para declarar os valores da saida.
                self.assertEqual(saida.descricao, "Pagamento de contas")#Aqui será verificado com a função (self.assertEqual) se o valor da saida (Descrição) está retornando corretamente.
                self.assertEqual(saida.valor, 50.0)#Aqui será verificado com a função (self.assertEqual) se o valor da entrada (Valor) está retornando corretamente.
                self.assertEqual(saida.tipo, "saida")#Aqui será verificado com a função (self.assertEqual) se o valor da entrada (Tipo) está retornando corretamente.
                
                # Verificar se as transações foram adicionadas
                transacoes = fm.listar_transacoes()#Aqui foi criado uma variavel para armazenar a lista de trasições
                self.assertEqual(len(transacoes), 2)#Aqui será verificado com a função(self.assertEqual) se a contagem de transições é igual a 2, para contar isso, é usado a função(len)
                self.assertEqual(transacoes[0].descricao, "Compra de alimentos")#Aqui será verificado com a função(self.assertEqual) se a transação de posição 0 é a descrição(Compra de alimentos)
                self.assertEqual(transacoes[1].descricao, "Pagamento de contas")#Aqui será verificado com a função(self.assertEqual) se a transação de posição 1 é a descrição(Pagamento de contas)
                
                # Testar o cálculo do saldo
                saldo = fm.calcular_saldo()#Aqui foi criado a variavel para armazenar a função (calcular_saldo).
                self.assertEqual(saldo, 50.0)  # 100 de entrada - 50 de saída
                
                # Testar a remoção de transação
                fm.remover_transacao(transacoes[0].id)#Aqui foi colocado a função fm.remover_transacao() para remover a transação de id 0
                self.assertEqual(len(fm.listar_transacoes()), 1)  # Aqui foi verificado se realmente resta apenas uma transação.

if __name__ == "__main__":
    unittest.main()