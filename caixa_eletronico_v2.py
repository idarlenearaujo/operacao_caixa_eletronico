import textwrap


def cadastrar_cliente(clientes):
    """
    Cadastrar cliente
    """
    cliente = {}

    cliente["cpf"] = input("\nDigite o CPF:")

    if not cpf_exists(cliente["cpf"], clientes):  # Conferência de cadastro
        cliente["nome"] = input("\nDigite o nome: ")
        cliente["data_nascimento"] = input("\nDigite data de nascimento: ")
        cliente["endereco"] = input(
            "\nDigite o endereco [Rua, número - Bairro - Cidade - UF]: "
        )

        clientes.append(cliente)  # Armazenando em uma lista
        print("\nCliente Cadastrado!\n")

    else:
        print("\nCPF já cadastrado!!!\n")


def cadastrar_conta(num_conta, clientes):
    """
    Cadastrando conta
    """
    conta = {}

    cpf = input("\nDigite o CPF do cliente: ")

    if cpf_exists(cpf, clientes):

        conta["cpf"] = cpf
        conta["agencia"] = "0001"
        conta["numero_conta"] = num_conta

        contas.append(conta)

        print("\nConta Cadastrada!\n")

    else:
        print("\nCPF não cadastrado!")


def listar_contas():
    """
    Listando contas
    """
    print("\n-------------------------------------------")
    print("----------------- CONTAS ------------------")
    print("-------------------------------------------")
    for conta in contas:
        print(f"CPF: {conta['cpf']}, Número da Conta: {conta['numero_conta']}")
    print("-------------------------------------------\n")


def listar_clientes():
    """
    Listando clientes
    """
    print("\n-------------------------------------------")
    print("---------------- CLIENTES -----------------")
    print("-------------------------------------------")
    for cliente in clientes:
        print(f"Nome: {cliente['nome']}, CPF: {cliente['cpf']}")
    print("-------------------------------------------\n")


def depositar_cash():
    """
    Depositar dinheiro: função para depositar na conta, \
    existe verificação de valores negativos
    """
    try:
        valor = float(input("\nDigite o valor a ser depositado: "))

        if valor > 0:  # verifica e se maior que 0 retorna valor para conta
            return valor

    except Exception as error:
        print(f"\nENTRADA INVÁLIDA!!!{error}")


def sacar_cash(valor_conta, saques_realizados):
    """
    Função para sacar na conta, existe a verificação se o valor a ser sacado \
    é possível.
    """
    if saques_realizados < 3:

        try:
            valor_saque = float(
                input("\nDigite o valor que deseja sacar: ")
            )  # recebe valor

            if (
                0 < valor_saque <= 500
            ):  # verifica se o saque é maior que 0 e se número de saques é
                # inferior a 3 e se o valor é menor ou igual a 500,00
                if valor_conta >= valor_saque:  # verifica se existe saldo
                    return valor_saque

                else:
                    print(
                        "\nSALDO INSUFICIENTE!!!"
                    )  # se conta não tem saldo suficiente para o saque,
                    # retorna mensagem de erro
            else:
                print(
                    "\nO valor informado não deve ser zero, valor negativo ou \
                        superior a R$ 500.00.\nInforme um valor válido."
                )
        except Exception as error:
            print(f"\nValor inválido informado. {error}\n")
    else:
        print("\nVocê atingiu o limite de 3 saques.")

    return 0


def extrato_cash(saldo):
    """
    Extrato
    """
    print("\n-------------------------------------------")
    print("----------------- EXTRATO -----------------")
    print("-------------------------------------------")

    for item in extrato:
        print(item)

    print(f"\nSaldo disponível: R$ {saldo:.2f}")
    print("-------------------------------------------\n")


def cpf_exists(cpf, clientes):
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            return True
    return False


if __name__ == "__main__":
    """
    Main chamada principal
    """
    print("Início do sistema Bancário!\n")

    # Variáveis
    clientes = []
    contas = []
    num_conta = 1
    valor_conta = 0
    extrato = []
    saques_realizados = 0

    while True:

        menu = """\n
        =============== MENU ===============
        [D]\tDepositar
        [S]\tSacar
        [E]\tExtrato
        [NC]\tNova Conta
        [NU]\tNovo Usuário
        [LC]\tListar Clientes
        [LCC]\tListar Contas
        [Q]\tSair
        """

        try:
            opcao = input(textwrap.dedent(menu)).upper()

            if opcao == "NU":

                cadastrar_cliente(clientes)

            elif opcao == "NC":

                cadastrar_conta(num_conta, clientes)
                num_conta += 1

            elif opcao == "LC":

                listar_clientes()

            elif opcao == "LCC":

                listar_contas()

            elif opcao == "D":

                valor_depositado = depositar_cash()
                valor_conta += valor_depositado
                extrato.append(f"Valor de R$ {valor_conta:.2f} depositado.")
                print(f"\nValor de R$ {valor_depositado:.2f} depositado.\n")

            elif opcao == "S":

                valor_sacado = sacar_cash(valor_conta, saques_realizados)

                if valor_sacado > 0:
                    valor_conta -= valor_sacado
                    extrato.append(f"Valor de R$ {valor_sacado:.2f} debitado.")
                    print(f"\nValor de R$ {valor_sacado:.2f} foi sacado.\n")
                    saques_realizados += 1

                else:
                    print("\nA quantidade de saque limite (3) foi atingida.")

            elif opcao == "E":
                extrato_cash(valor_conta)
            elif opcao == "Q":
                print(
                    "\nSaindo da sua conta!\n\n# # # # # # # # # # # # # #"
                )
                break
            else:
                print("\nOpção inválida. Tente novamente.\n")

        except Exception as error:
            print(f"\nOpção inválida. Tente novamente. {error}\n")
