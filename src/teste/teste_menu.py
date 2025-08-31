import unittest  
import sys  
import os  
from unittest.mock import patch  
from io import StringIO  
from io import BytesIO  


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.main import menu  # Importa a função 'menu' do arquivo 'main.py' que está no diretório 'src'.


class TestMenu(unittest.TestCase):

    # Simula o comportamento do usuário, fornecendo entradas para o menu.
    @patch("builtins.input", side_effect=["1", "Compra de alimentos", "100", "0"])  # Simula a entrada do usuário: "1", "Compra de alimentos", "100", "0".
    @patch("sys.stdout", new_callable=StringIO)  # Captura tudo o que seria impresso no terminal, redirecionando para 'StringIO'.
    def test_adicionar_entrada(self, mock_stdout, mock_input):
        menu()  # Chama a função 'menu', que será testada, usando as entradas simuladas.

        
        output = mock_stdout.getvalue()  # Captura tudo o que foi impresso durante a execução do menu.

        
        self.assertIn("✅ Entrada adicionada!", output)# Verifica se a mensagem de sucesso foi impressa após a adição de uma entrada.
        self.assertIn("1. Adicionar entrada", output)  # Verifica se a opção do menu "Adicionar entrada" foi impressa corretamente após a interação do usuário.

    
    @patch("builtins.input", side_effect=["2", "Pagamento de contas", "50", "0"])  # Simula a entrada do usuário: "2", "Pagamento de contas", "50", "0".
    @patch("sys.stdout", new_callable=StringIO)  # Captura tudo o que seria impresso no terminal, redirecionando para 'StringIO'.
    def test_adicionar_saida(self, mock_stdout, mock_input):
        menu()  # Chama a função 'menu', que será testada, usando as entradas simuladas.

        
        output = mock_stdout.getvalue()# Captura tudo o que foi impresso durante a execução do menu.

        
        self.assertIn("✅ Saída adicionada!", output)# Verifica se a mensagem de sucesso foi impressa após a adição de uma saída.

    
    @patch("builtins.input", side_effect=["3", "0"])  # Simula a entrada do usuário: "3", "0".
    @patch("sys.stdout", new_callable=StringIO)  # Captura tudo o que seria impresso no terminal, redirecionando para 'StringIO'.
    def test_listar_transacoes(self, mock_stdout, mock_input):
        menu()  # Chama a função 'menu', que será testada, usando as entradas simuladas.

        
        output = mock_stdout.getvalue()# Captura tudo o que foi impresso durante a execução do menu.

        
        self.assertIn("Compra de alimentos", output) # Verifica se uma transação foi listada corretamente, procurando pela descrição "Compra de alimentos".

    
    @patch("builtins.input", side_effect=["4", "0"])  # Simula a entrada do usuário: "4", "0".
    @patch("sys.stdout", new_callable=StringIO)  # Captura tudo o que seria impresso no terminal, redirecionando para 'StringIO'.
    def test_ver_saldo(self, mock_stdout, mock_input):
        menu()  # Chama a função 'menu', que será testada, usando as entradas simuladas.

        
        output = mock_stdout.getvalue()# Captura tudo o que foi impresso durante a execução do menu.

        
        self.assertIn("💰 Saldo atual: R$", output)# Verifica se o saldo foi impresso corretamente na saída.

    
    @patch("builtins.input", side_effect=["5", "1", "0"])  # Simula a entrada do usuário: "5", "1", "0".
    @patch("sys.stdout", new_callable=StringIO)  # Captura tudo o que seria impresso no terminal, redirecionando para 'StringIO'.
    def test_remover_transacao(self, mock_stdout, mock_input):
        menu()  # Chama a função 'menu', que será testada, usando as entradas simuladas.

        
        output = mock_stdout.getvalue()# Captura tudo o que foi impresso durante a execução do menu.

        
        self.assertIn("ID não encontrado.", output)# Verifica se a mensagem de erro foi impressa quando não há transação com o ID fornecido.

    
    @patch("builtins.input", side_effect=["0"])  # Simula a entrada do usuário: "0" para sair.
    @patch("sys.stdout", new_callable=StringIO)  # Captura tudo o que seria impresso no terminal, redirecionando para 'StringIO'.
    def test_sair(self, mock_stdout, mock_input):
        menu()  # Chama a função 'menu', que será testada, usando as entradas simuladas.

        
        output = mock_stdout.getvalue()# Captura tudo o que foi impresso durante a execução do menu.

        
        self.assertIn("Saindo...", output)# Verifica se a mensagem "Saindo..." foi impressa após a opção de sair ser escolhida.


if __name__ == "__main__": # Se o arquivo for executado diretamente, o código de teste será rodado.
    unittest.main()  # Roda os testes e exibe os resultados no terminal.
