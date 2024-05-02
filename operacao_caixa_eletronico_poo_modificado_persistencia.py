import os
import re
import textwrap
from abc import ABC, abstractclassmethod
from datetime import datetime
from pathlib import Path


class Banco:
    """
    Classe que representa o Banco, contendo as contas e clientes

    Caso seja a primeira execução irá retornar listas vazias,
    caso contrário, irá buscar do arquivo log.txt e alimentar
    as variavéis clientes e contas.


    Parâmetros:
        clientes -> Uma lista contendo todos os clientes cadastrados
        contas -> Uma lista contendo todas as contas cadastradas

    Métodos:
        clientes -> acessar variável privada
        contas -> acessar variável privada
        carregar_dados -> Recebe o arquivo de log
        para carregar os clientes e contas armazenadas anteriormente
        main -> Inicialização do programa do Banco
    """
    def __init__(self):
        """
        Inicializando clientes e contas
        """
        self._clientes = []
        self._contas = []

    @property
    def clientes(self):
        return self._clientes

    @property
    def contas(self):
        return self._contas

    def carregar_dados(self, arquivo):
        """
        Função que carrega os dados nas variáveis clientes e contas
        """
        try:

            with open(arquivo, "r") as arquivo:

                for linha in arquivo:

                    pf = re.findall(r"PessoaFisica: \(([^)]+)\)", linha)
                    cc = re.findall(r"ContaCorrente: \(([^)]+)\)", linha)

                    for texto in pf:
                        texto = texto.replace("'", "").replace(" ", "")
                        texto = texto.split(",")

                        cpf, nome = str(texto[0]), str(texto[1])

                        if (cpf not in
                                [cliente.cpf for cliente in self.clientes]):

                            self._clientes.append(
                                PessoaFisica("", cpf, nome, ""))

                    for texto in cc:
                        texto = texto.replace("'", "").replace(" ", "")
                        texto = texto.split(",")

                        numero, cpf_cliente = int(texto[1]), texto[3]

                        match_cli = next(
                                (cli for cli in self.clientes
                                 if cli.cpf == cpf_cliente),
                                None
                            )

                        if (match_cli and
                                numero not in [conta.numero
                                               for conta in self.contas]):

                            conta = ContaCorrente.nova_conta(match_cli, numero)

                            self._contas.append(conta)
                            match_cli.adicionar_conta(conta)

                return self.clientes, self.contas

        except IOError as error:
            print(f"Erro: {error}")

    def main(self):

        while True:

            opcao = menu()

            if opcao == "D":
                depositar(self.clientes)
            elif opcao == "S":
                sacar(self.clientes)
            elif opcao == "E":
                extrato(self.clientes)
            elif opcao == "NC":
                numero_conta = len(self.contas) + 1
                criar_contas(numero_conta, self.clientes, self.contas)
            elif opcao == "NU":
                criar_cliente(self.clientes)
            elif opcao == "LC":
                listar_contas(self.contas)
            elif opcao == "Q":
                return False
            else:
                print("\n@@@ Opção inválida! Digite uma opção válida! @@@")


class ContaIterador:
    """
    Iterador para a classe Conta
    """
    def __init__(self, contas):
        """
        Inicializando o iterador

        Parâmetros:
        contas (list): Lista de contas
        """
        self._contas = contas
        self._index = 0

    def __iter__(self):
        """
        Retorna o iterador atual
        """
        return self

    def __next__(self):
        """
        Retorna a próxima conta da lista

        StopIteration se não houver mais conta na lista
        """
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
    """
    Classe que representa um cliente de um banco
    """
    def __init__(self, endereco):
        """
        Inicializando um cliente com um endereço e uma lista vazia de contas
        """
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        """
        Método que realiza uma transação para uma conta específica
        com o condicional limite de 10 transações

        conta (Conta): A conta na qual a transação será realizada
        transacao (Transacao): A transação que será realizada
        """
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n@@@ Você excedeu o número de transações para hoje! @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """
        Adiciona a conta a lista de contas do cliente

        conta (Conta): A conta a ser adicionada
        """
        self.contas.append(conta)

    def __iter__(self):
        """
        Retorna o iterador para as contas do cliente
        """
        return ContaIterador(self.contas)


class PessoaFisica(Cliente):
    """
    Classe que representa um cliente do banco que é pessoa física.
    """
    def __init__(self, endereco, cpf, nome, data_nascimento):
        """
        Inicializa uma pessoa física com um endereço, CPF, nome e data de
        nascimento
        """
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def __repr__(self) -> str:
        """
        Retorna uma representação de string da pessoa física
        """
        return f"{self.__class__.__name__}: ({self.cpf}, '{self.nome}')"


class Conta:
    """
    Classe que representa uma conta no banco de um cliente
    """
    def __init__(self, numero, cliente):
        """
        Inicializando uma conta com o cliente,
        agência com o valor fixo "4034",
        número da conta que será incrementado +1,
        saldo com o valor inicial 0
        e o historico das transações
        """
        self._cliente = cliente
        self._agencia = "4034"
        self._numero = numero
        self._saldo = 0.0
        self._historico = Historico()

    # Métodos
    @classmethod
    def nova_conta(cls, cliente, numero):
        """
        Método de classe para criar uma nova conta
        """
        return cls(numero, cliente)

    """
    Métodos getters para acessar atributo privado
    """
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
        """
        Método de classe para sacar valor da conta

        Verifica se em saldo há o valor necessário para sacar
        Se sim, verifica se o valor a sacar é maior que 0
        Se sim, o valor é decrementado em saldo e retorna True
        e a mensagem de saque realizado com sucesso.
        """
        saldo = self.saldo
        valor_final = valor > saldo

        if valor_final:
            print("\n@@ Operação falhou! Você não tem saldo suficiente. @@")

        else:

            if valor > 0:
                self._saldo -= valor
                print("\n=========== Saque realizado com sucesso! ===========")
                return True

            else:
                print("\n@@ Operação falhou! O valor informado é inválido. @@")

        return False

    def depositar(self, valor):
        """
        Método de classe para depositar valor da conta
        Verifica se o valor a ser depositado é maior que 0
        Se sim, o valor é incrementado em saldo e uma mensagem
        de depósito realizado é mostrado e retorna True.
        """
        if valor > 0:
            self._saldo += valor
            print("\n=========== Depósito realizado com sucesso! ============")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido! @@@")
            return False


class ContaCorrente(Conta):
    """
    Classe que representa uma subclasse de Conta
    """
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        """
        Inicializando classe com:
        limite de saque para a conta corrente = $500
        limite de saques permitidos = 3
        lista para armazenar os saques realizados
        """
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.lista_saques = []

    def sacar(self, valor):
        """
        Método para sacar um valor da conta corrente, com verificações
        adicionais para limite de saque e número de saques.
        """

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
        """
        Representação utilizado no LOG
        """
        return (
            f"{self.__class__.__name__}: "
            f"('{self.agencia}', "
            f"'{self.numero}', "
            f"'{self.cliente.nome}', "
            f"'{self.cliente.cpf}')"
        )

    def __str__(self):
        """
        Representação legível da conta corrente
        """
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    """
    Classe que representa o Historico das transações
    """
    def __init__(self):
        """
        Iniciando classe com uma lista vazia chamada
        transacao, onde ficará armazenado as transações
        """
        self._transacoes = []

    # Métodos
    @property
    def transacoes(self):
        """
        Get do atributo privado transacoes
        """
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Método que adiciona a lista o tipo da transação,
        o valor e a data.
        """
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
    """
    Classe abstrata Transacao, com os métodos que suas
    subclasses devem implementar
    """
    @property
    @abstractclassmethod
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self):
        pass


class Saque(Transacao):
    """
    Subclasse do tipo Transacao, representa um tipo de Transacao
    com os métodos próprios
    """
    def __init__(self, valor):
        """
        Inicializando classe com o atributo valor
        """
        self._valor = valor

    @property
    def valor(self):
        """
        Get do atributo valor
        """
        return self._valor

    def registrar(self, conta):
        """
        Método para registrar a transacao na Classe
        Conta utilizando o método sacar.
        Neste método se o valor_final é maior que 0,
        este valor é decrementado em saldo (Conta)
        e é retornado True e é efetivado a transação.
        Caso contrário um erro de saldo insuficiente
        é mostrado.
        """
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """
    Subclasse do tipo Transacao, representa um tipo de Transacao
    com os métodos próprios
    """
    def __init__(self, valor):
        """
        Inicializando classe com o atributo valor
        """
        self._valor = valor

    @property
    def valor(self):
        """
        Get do atributo valor
        """
        return self._valor

    def registrar(self, conta):
        """
        Método para registrar a transacao na Classe
        Conta utilizando o método depositar.
        Neste método se o valor é maior que 0,
        este valor é incrementado em saldo (Conta)
        e é retornado True e é efetivado a transação.
        """
        sucesso_deposito = conta.depositar(self._valor)

        if sucesso_deposito:
            conta.historico.adicionar_transacao(self)


def impressoes(impress):
    """
    Função para escrever o log em um txt
    """
    with open(ROOT_PATH / "log.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(impress)


def log_transacao(func):
    """
    Decorador
    """
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
    """
    Verifica se existe o cpf em clientes
    """
    cliente_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrados[0] if cliente_filtrados else None


def filtrar_contas(cliente):
    """
    Verifica se há contas cadsatradas para o cliente
    """
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    return cliente.contas[0]


@log_transacao
def criar_cliente_conta(clientes, cpf, contas, num_conta, transacao):

    cliente = filtrar_clientes(cpf, clientes)

    if cliente and transacao == 'cliente':
        print("\n@@@ Já existe cliente para este CPF. @@@")
        return

    elif not cliente and transacao == 'cliente':
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe data de nascimento(dd-mm-aaaa): ")
        endereco = input("Informe (Rua, Nº - Bairro - Cidade/Estado)")

        clientes.append(PessoaFisica(endereco, cpf, nome, data_nascimento))
        print("\n=========== Cliente cadastrado com sucesso! ============")
        return

    elif not cliente and transacao == 'conta':
        print("\n@@ Cadastre um cliente antes de adicionar uma conta. @@ ")
        return

    elif cliente and transacao == 'conta':
        conta = ContaCorrente.nova_conta(cliente, num_conta)
        contas.append(conta)
        cliente.adicionar_conta(conta)

        print("\n================ Conta criada com sucesso! =================")
        return

    else:
        print("\n@@@ Tipo de transação inválido. @@@")
        return


def criar_contas(numero_contas, clientes, contas):
    """
    Criando uma nova conta para um cliente
    """
    cpf = input("Informe o CPF do cliente: ")
    criar_cliente_conta(clientes, cpf, contas, numero_contas, "conta")


def criar_cliente(clientes):
    """
    Criando um novo cliente
    """
    cpf = input("Informe o CPF do cliente: ")
    criar_cliente_conta(clientes, cpf, [], 0, 'cliente')


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
def transacao_saque_deposito(clientes, cpf, valor, tipo_transacao):

    """
    Função responsável por gerenciar a função sacar e depositar
    Esta função irá checar em filtrar_clientes se o cpf está na
    lista de clientes e se existe conta para aquele cpf.
    Caso positivo, o saque será feito e o deposito será feito,
    dependendo do parâmentro informado.
    """

    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Não existe cliente para este CPF. @@@")
        return

    conta = filtrar_contas(cliente)

    if not conta:
        print("\n@@@ Não existe conta cadastrada para esse cliente! @@@")
        return

    if tipo_transacao == 'sacar':
        transacao = Saque(valor)
    elif tipo_transacao == 'depositar':
        transacao = Deposito(valor)
    else:
        print("\n@@@ Tipo de transação inválido. @@@")
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    """
    Função responsável por decrementar saldo em Conta
    """
    cpf = input("Informe o CPF do cliente: ")
    valor = float(input("Digite o valor que deseja sacar: "))
    transacao_saque_deposito(clientes, cpf, valor, 'sacar')


def depositar(clientes):
    """
    Função responsável por incrementar saldo em Conta
    """
    cpf = input("Informe o CPF do cliente: ")
    valor = float(input("Digite o valor que deseja depositar: "))
    transacao_saque_deposito(clientes, cpf, valor, 'depositar')


def listar_contas(contas):
    """
    Função que lista todas as contas já cadastradas
    """
    if len(contas) > 0:
        for conta in ContaIterador(contas):
            print("=" * 100)
            print(textwrap.dedent(str(conta)))
    else:
        print("\n@@@ Não há contas cadastradas! @@@")


if __name__ == "__main__":
    """
    Inicializando o programa Banco

    ROOT_PATH: Caminho do arquivo de log
    banco: Contém o objeto banco que contém
    lista de clientes e contas recuperadas

    Se o arquivo log existe e seu tamanho é superior a 0,
    então carrega os dados no objeto banco e continua a
    execução do sistema.
    """

    ROOT_PATH = Path(__file__).parent
    banco = Banco()

    if (os.path.exists(ROOT_PATH / "log.txt") and
            os.path.getsize(ROOT_PATH / "log.txt") > 0):
        banco.carregar_dados(ROOT_PATH / "log.txt")

    banco.main()
