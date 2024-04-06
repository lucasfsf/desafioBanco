import re

class User:
    cpfs = []

    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = self.verify_cpf(cpf) # main_id
        if not self.cpf:
            print("Cpf ja cadastrado ou invalido. Verificar.")
            return
        self.endereco = endereco
        self.cpfs.append(self.cpf)

    def verify_cpf(self, cpf):
        # Define regular expression pattern to match non-digit characters
        pattern = r'\D'
        # Remove all non-digit characters and white spaces
        clean_cpf = re.sub(pattern, '', cpf)
        if clean_cpf in self.cpfs:
            return None
        else:
            return clean_cpf
  
class Conta:
    """Cria conta de banco com funções de extrato, depósito e saque.
    """
    agencia = "0001"
    cont_conta = 0
    menu = """
    MENU
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    def __init__(self, usuario, saldo = 0):
        self.saldo = saldo
        self.extrato = ""
        self.numero_saques = 0
        self.limite = 500
        self.usuario = usuario
        self.numero_conta = self.cont_conta + 1

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
        return f"{self.usuario.nome} - Saldo da conta: {self.saldo}\n"

      
def main():
    users = []
    user = User("João Testador", "01/09/1999", "086.546.325-96", "Rua Teste, 14 - Jaboão - Belo Horizonte/MG")
    users.append(user)
    conta = Conta(user)
    print(conta)
    while True:
        opcao = input(conta.menu)
        if opcao == "q":
            break
        else: 
             conta.operacao(opcao)

if __name__ == "__main__":
    main()