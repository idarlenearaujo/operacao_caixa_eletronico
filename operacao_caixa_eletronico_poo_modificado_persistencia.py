import os
import re
import textwrap
from abc import ABC, abstractclassmethod
from datetime import datetime
from pathlib import Path


ROOT_PATH = Path(__file__).parent


class ContaIterador:
    def __init__(self, contas):
        self._contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self._contas[self._index]
            return f"""\
            {conta}
            """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    # Métodos
    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n@@@ Você excedeu o número de transações para hoje! @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __iter__(self):
        return ContaIterador(self.contas)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: ({self.cpf}, '{self.nome}')"


class Conta:
    def __init__(self, numero, cliente):
        self._cliente = cliente
        self._agencia = "4034"
        self._numero = numero
        self._saldo = 0.0
        self._historico = Historico()

    # Métodos
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
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

    def sacar(self, valor):

        # Checando se há valor para sacar
        saldo = self.saldo
        valor_final = valor > saldo

        if valor_final:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        if valor > 0:
            self._saldo -= valor
            print("\n============= Saque realizado com sucesso! =============")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):

        if valor > 0:
            self._saldo += valor
            print("\n=========== Depósito realizado com sucesso! ============")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido! @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.lista_saques = []

    def sacar(self, valor):
        for transacao in self.historico.transacoes:
            if transacao["tipo"] == Saque.__name__:
                self.lista_saques.append(transacao)

        numero_saques = len(self.lista_saques)

        excedeu_limmite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limmite:
            print("\n@@ Operação falhou! Excedeu o valor limite de saque! @@")

        if excedeu_saques:
            print("\n@@ Excedeu a quantidade de operaçãoes permitidas! @@")

        if not excedeu_limmite and not excedeu_saques:
            return super().sacar(valor)

        return False

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: "
            f"('{self.agencia}', "
            f"'{self.numero}', "
            f"'{self.cliente.nome}', "
            f"'{self.cliente.cpf}')"
        )

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            CPF:\t{self.cliente.cpf}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    # Métodos
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y  %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now()
        transacoes = []
        masc = "%d-%m-%Y %H:%M:%S"

        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], masc).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)

        return transacoes


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


def impressoes(impress):
    with open(ROOT_PATH / "log.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(impress)


def carregar_dados(arquivo):

    clientes = []
    contas = []

    try:
        # Abrindo o arquivo para realizar a leitura dos dados
        with open(arquivo, "r") as arquivo:

            for linha in arquivo:

                # selecionando apenas dados com PessoaFisica
                p_Fisica = re.findall(r"PessoaFisica: \(([^)]+)\)", linha)
                # selecionando dados apenas com ContaCorrente
                c_Corrente = re.findall(r"ContaCorrente: \(([^)]+)\)", linha)

                for x in p_Fisica:
                    x = x.replace("'", "").replace(" ", "")
                    x = x.split(",")
                    # Parametrizando layout para inserir um novo objeto
                    x = [str(x[0]), str(x[1])]
                    if x[0] not in [cliente.cpf for cliente in clientes]:
                        # novo objeto e novo item na lista
                        clientes.append(PessoaFisica("", x[0], x[1], ""))

                for x in clientes:
                    # Filtrando cliente por cliente
                    cliente = filtrar_clientes(x.cpf, clientes)

                    for i in c_Corrente:
                        i = i.replace("'", "").replace(" ", "")
                        i = i.split(",")
                        # Paramentrizando layout de ContaCorrente
                        i = [str(i[0]), int(i[1]), str(i[2]), str(i[3])]

                        match_cli = next(
                            (cli for cli in clientes if cli.cpf == i[3]), None
                        )

                        if (match_cli and
                            i[1] not in
                                [conta.numero for conta in contas]):
                            # Criando um novo objeto ContaCorrente
                            conta = ContaCorrente.nova_conta(match_cli, i[1])
                            # Adicionando conta na lista de contas
                            contas.append(conta)
                            cliente.adicionar_conta(conta)

            return clientes, contas

    except FileNotFoundError:
        print("Arquivo não encontrado!")


def log_transacao(func):
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        impress = f"{data_hora}|{func.__name__}|{args}|{kwargs}|{result}\n"

        impressoes(impress)

        return result

    return wrapper


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


@log_transacao
def criar_contas(numero_contas, clientes, contas):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@ Cadastre um cliente antes de adicionar uma conta. @@ ")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_contas)

    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n================== Conta criada com sucesso! ==================")


@log_transacao
def criar_cliente(clientes):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente para este CPF. @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe (Logradouro, Número - Bairro - Cidade/Estado)")

    clientes.append(PessoaFisica(endereco, cpf, nome, data_nascimento))

    print("\n=============== Cliente cadastrado com sucesso! ===============")


@log_transacao
def extrato(clientes):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não cadastrado! @@@")
        return

    conta = filtrar_contas(cliente)

    if not conta:
        print("\n@@@ O cliente não tem conta cadastrada! @@@")
        return

    print("\n====================== EXTRATO ======================")
    extrato = ""
    tem_transacao = False

    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        if transacao["tipo"] == "Saque":
            data = transacao["data"]
            tipo = transacao["tipo"]
            valor = transacao["valor"]
            extrato += f"{data}\t{tipo}\t\tR$ {valor:.2f}\n"
        else:
            data = transacao["data"]
            tipo = transacao["tipo"]
            valor = transacao["valor"]
            extrato += f"{data}\t{tipo}\tR$ {valor:.2f}\n"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações!"

    print(extrato)
    print(f"\nSaldo:\t\t\t\t\tR$ {conta.saldo:.2f}")
    print("======================================================")


@log_transacao
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


@log_transacao
def depositar(clientes):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Não existe cliente para este CPF. @@@")
        return

    valor = float(input("Digite o valor que deseja depositar: "))

    transacao = Deposito(valor)
    conta = filtrar_contas(cliente)

    if not conta:
        print("\n@@ Não existe conta cadastrada para esse cliente! @@")
        return

    cliente.realizar_transacao(conta, transacao)


def listar_contas(contas):

    if len(contas) > 0:
        for conta in ContaIterador(contas):
            print("=" * 100)
            print(textwrap.dedent(str(conta)))
    else:
        print("\n@@@ Não há contas cadastradas! @@@")


def main(cli, cont):

    clientes = cli
    contas = cont

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
            criar_contas(numero_conta, clientes, contas)
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

    clientes = []
    contas = []

    if os.path.exists(ROOT_PATH / "log.txt"):
        if os.path.getsize(ROOT_PATH / "log.txt") > 0:
            clientes, contas = carregar_dados(ROOT_PATH / "log.txt")

    else:

        clientes = []
        contas = []

    main(clientes, contas)
