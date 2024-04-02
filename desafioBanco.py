class Conta:
    """Cria conta de banco com funções de extrato, depósito e saque.
    """
    menu = """
    MENU
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    def __init__(self, saldo = 0):
        self.saldo = saldo
        self.extrato = ""
        self.numero_saques = 0
        self.limite = 500

    def operacao(self, opcao):
        if opcao == "d":
            self.deposito()
        elif opcao == "s":
            self.saque()    
        elif opcao == "e":
            self.imprimir_extrato()
        else:
            print("Operação falhou! O valor informado é inválido.")

    def deposito(self):
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Operação falhou! O valor informado é inválido.")

    def saque(self, limite_saques = 3):
        valor = float(input("Informe o valor do saque: "))

        if valor > self.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif valor > self.limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif self.numero_saques >= limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    def imprimir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")

    def __add__(self, other):
        nova_conta = Conta(saldo = self.saldo + other.saldo)
        return nova_conta
    
    def __str__(self):
        return f"Saldo da conta: {self.saldo}\n"

def main():
    conta = Conta()
    while True:
        opcao = input(conta.menu)
        if opcao == "q":
            break
        else: 
             conta.operacao(opcao)

if __name__ == "__main__":
    main()