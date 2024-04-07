import textwrap
from abc import ABC, abstractmethod
import re
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero_conta, cliente):
        return cls(numero_conta, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero_conta(self):
        return self._numero_conta
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False

        elif valor > 0:
            self._saldo -= valor
            return True

        else:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
            )
        
        if valor > self.limite:
            print("Você excedeu seu limite de saque de {self.limite}.")
        elif numero_saques > self.limite_saques:
            print("Você excedeu seu limite de saques de {self.limite_saques}.")
        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
            Agência:\t {self.agencia}
            C/C:\t\t {self.numero_conta}
            Titular:\t {self.cliente.nome}
        """ 

class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes    
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """\n
        MENU
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nc] Nova Conta
        [lc] Listar Contas
        [nu] Novo Usuário
        [q] Sair
        => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def escolher_conta(contas):
    for i, conta in enumerate(contas):
        print(f"{i} - {conta.numero_conta}")

    conta_escolhida = input("Operação em qual conta: ")
    if conta_escolhida not in contas:
        return None
    else:
        return conta_escolhida

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui contas nesse banco.")
        return
    if len(cliente.contas) == 1:
        return cliente.contas[0]
    else: 
        return escolher_conta(cliente.contas)
    
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    # limpar input para remover simbolos
    pattern = r'\D'
    clean_cpf = re.sub(pattern, '', cpf)

    cliente = filtrar_cliente(clean_cpf, clientes)

    if cliente:
        print("\nCpf ja cadastrado. Verificar.")
        return
    
    # Criar o cliente
    nome = input("Nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=clean_cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso.")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente,numero_conta=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso.")

def listar_contas(contas):
    for conta in contas:
        print("*" * 100)
        print(textwrap.dedent(str(conta)))

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return
    
    valor = float(input("Informe o valor de depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return
    
    valor = float(input("Informe o valor de saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n\tR$ {transacao["valor"]:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break 
        else:
            print("Opção Inválida.")
         
if __name__ == "__main__":
    main()