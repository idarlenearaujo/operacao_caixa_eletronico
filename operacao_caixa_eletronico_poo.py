from abc import ABC, abstractclassmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    # Métodos
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, numero, cliente):
        self._cliente = cliente
        self._agencia = "4034"
        self._numero = numero
        self._saldo = 0.0
        self._historico = Historico()

    # Métodos
    @ property
    def saldo(self):
        return self._saldo

    @property
    def cliente(self):
        return self._cliente

    @property
    def agencia(self):
        return self._agencia

    @property
    def numero(self):
        return self._numero

    @property
    def historico(self):
        return self._historico

    @classmethod    
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    def sacar(self, valor):
        
        # Checando se há valor para sacar
        valor_final = self._saldo - valor

        if valor_final >= 0:
            self._saldo -= valor
            print("\n=============== Saque realizado com sucesso! ===============")
            return True

        else:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente! @@@")
            return False

    def depositar(self, valor):

        if valor > 0:
            self._saldo += valor
            print("\n=============== Depósito realizado com sucesso! ===============")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido! @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )

        excedeu_limmite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limmite:
            print("\n@@@ Operação falhou! Excedeu o valor limite de saque! @@@")

        if excedeu_saques:
            print("\n@@@ OPeração falhou! Excedeu a quantidade de operaçãoes permitidas! @@@")
        
        if not excedeu_limmite and not excedeu_saques:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Historico:
    def __init__(self):
        self._transacoes = []

    # Métodos
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {"tipo": transacao.__class__.__name__,
             "valor": transacao.valor,
             "data": datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
            }
        )

class Transacao(ABC):
    
    @property
    @abstractclassmethod
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_deposito = conta.depositar(self._valor)

        if sucesso_deposito:
            conta.historico.adicionar_transacao(self)

def menu():

    menu = """\n
    =============== MENU ===============
    [D]\tDepositar
    [S]\tSacar
    [E]\tExtrato
    [NC]\tNova Conta
    [NU]\tNovo Usuário
    [LC]\tListar Contas
    [Q]\tSair
    """

    return input(textwrap.dedent(menu)).upper()

def filtrar_clientes(cpf, clientes):
    cliente_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrados[0] if cliente_filtrados else None

def filtrar_contas(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    
    return cliente.contas[0]

def criar_contas(numero_contas, clientes, contas):
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não cadastrado, por favor cadastre um cliente antes de adicionar uma conta. @@@ ")
        return 
    
    conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero_contas)

    contas.append(conta)
    cliente.contas.append(conta)

    print("\n==================== Conta criada com sucesso! ====================")

def criar_cliente(clientes):
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente para este CPF. @@@")

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Logradouro, Número - Bairro - Cidade/Estado)")

    clientes.append(PessoaFisica(cpf = cpf, nome = nome, data_nascimento = data_nascimento, endereco = endereco))

    print("\n==================== Cliente cadastrado com sucesso! ====================")

def extrato(clientes):
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf = cpf, clientes = clientes)

    if not cliente:
        print("\n@@@ Cliente não cadastrado! @@@")
        return 
    
    conta = filtrar_contas(cliente)

    if not conta:
        print("\n@@@ O cliente não tem conta cadastrada! @@@")
        return 
    
    print("\n==================== EXTRATO ====================")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações!"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=====================================================")

def sacar(clientes):
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Não existe cliente para este CPF. @@@")
        return
    
    valor = float(input("Digite o valor que deseja sacar: "))
    transacao = Saque(valor)

    conta = filtrar_contas(cliente)

    if not conta:
        print("\n@@@ Não existe conta cadastrada para esse cliente! @@@")
        return
    
    cliente.realizar_transacao(conta, transacao)

def depositar(clientes):
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Não existe cliente para este CPF. @@@")
        return
    
    valor = float(input("Digite o valor que deseja sacar: "))
    transacao = Deposito(valor)

    conta = filtrar_contas(cliente)

    if not conta:
        print("\n@@@ Não existe conta cadastrada para esse cliente! @@@")
        return
    
    cliente.realizar_transacao(conta, transacao)

def listar_contas(contas):
    
    if len(contas) > 0:
        for conta in contas:
            print("=" * 100)
            print(textwrap.dedent(str(conta)))
    else:
        print("\n@@@ Não há contas cadastradas! @@@")

def main():

    # Listas que armazenam n clientes e contas
    clientes = []
    contas = []

    while True:
        
        opcao = menu()

        if opcao == "D":
            depositar(clientes)
        elif opcao == "S":
            sacar(clientes)
        elif opcao == "E":
            extrato(clientes)
        elif opcao == "NC":
            numero_conta = len(contas) + 1
            criar_contas(numero_contas = numero_conta, contas = contas, clientes = clientes)
        elif opcao == "NU":
            criar_cliente(clientes)
        elif opcao == "LC":
            listar_contas(contas)
        elif opcao == "Q":
            return False
        else:
            print("\n@@@ Opção inválida! Digite uma opção válida! @@@")


# Iniciando o programa

if __name__ == "__main__":

    main()