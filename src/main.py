from src.services.finance_manager import FinanceManager

def menu():
    fm = FinanceManager()

    while True:
        print("\n--- Controle Financeiro ---")
        print("1. Adicionar entrada")
        print("2. Adicionar saída")
        print("3. Listar transações")
        print("4. Ver saldo")
        print("5. Remover transação")
        print("0. Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            descricao = input("Descrição: ").strip()
            valor = float(input("Valor: ").strip())
            fm.adicionar_transacao("entrada", descricao, valor)
            print("✅ Entrada adicionada!")
        elif opcao == "2":
            descricao = input("Descrição: ").strip()
            valor = float(input("Valor: ").strip())
            fm.adicionar_transacao("saida", descricao, valor)
            print("✅ Saída adicionada!")
        elif opcao == "3":
            trans = fm.listar_transacoes()
            if not trans:
                print("Nenhuma transação.")
            for t in trans:
                print(f"{t.id} | {t.data} | {t.tipo:<7} | {t.descricao} | R$ {t.valor:.2f}")
        elif opcao == "4":
            print(f"💰 Saldo atual: R$ {fm.calcular_saldo():.2f}")
        elif opcao == "5":
            tid = int(input("ID da transação: ").strip())
            ok = fm.remover_transacao(tid)
            print("🗑️ Removida!" if ok else "ID não encontrado.")
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
