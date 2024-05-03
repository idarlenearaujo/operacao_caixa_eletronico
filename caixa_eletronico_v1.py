def depositar_cash(valor_conta):
    """
    Função: para depositar na conta, existe verificação de valores negativos
    """

    try:
        valor_deposito = float(input("\nDigite o valor para depositar: "))

        if valor_deposito > 0:
            return valor_deposito

    except Exception as error:
        print(f'\nENTRADA INVÁLIDA!!! {error}')


def sacar_cash(valor_conta, saques_realizados):
    """
    Função: para sacar na conta, existe a verificação se o valor a ser sacado
    é possível
    """

    if saques_realizados < 3:

        try:
            valor_saque = float(input("\nDigite o valor que deseja sacar: "))

            if 0 < valor_saque <= 500:
                if valor_conta >= valor_saque:
                    return valor_saque                
                else:
                    print("\nSALDO INSUFICIENTE!!!")
            else:
                print('\nO valor informado não deve ser zero, \
                      valor negativo ou superior a R$ 500.00.\n \
                      Informe um valor válido.')            
        except Exception as error:
            print(f'{error}')
    else:
        print('\nVocê atingiu o limite de 3 saques.')
    return 0


def extrato_cash(valor_conta, historico_conta):
    """
    Função: mostra extrato de todas as movimentação da conta ativa
    """

    for dados in historico_conta:
        print(dados)

    print(f"\nValor em conta atualizado: R$ {valor_conta:.2f}")


if __name__ == '__main__':
    """
    Version 1.0
    Main chamada principal
    """

    print('Início do sistema Bancário!\n')

    """
    Variáveis
    """
    hist_conta = []
    vl_conta = 0
    opcao = -1
    saques_realizados = 0

    """
    Loop simulando um caixa eletrônico
    Deposito - 1
    Saque - 2
    Extrato - 3
    Sair - 0
    """
    while True:

        print('------------------------------------------')
        print('----------- BEM VINDO AO BANCÃO ----------')
        print('------------------------------------------')
        print('Digite 1 - Depositar Valor')
        print('Digite 2 - Sacar Valor')
        print('Digite 3 - Extrato Completo')
        print('Digite 0 - Para Sair')

        try:
            opcao = int(input("\nOpção: "))

            if opcao == 1:

                vl_deposito = depositar_cash(vl_conta)
                vl_conta += vl_deposito
                hist_conta.append(f"Valor de +R$ {vl_deposito:.2f} creditado")
                print(f'\nValor R$ {vl_deposito:.2f} foi depositado.\n')

            elif opcao == 2:

                vl_sacado = sacar_cash(vl_conta, saques_realizados)

                if vl_sacado > 0:
                    vl_conta -= vl_sacado
                    hist_conta.append(f"Valor de -R$ {vl_sacado:.2f} debitado")
                    print(f'\nValor R$ {vl_sacado:.2f} foi sacado.\n')
                    saques_realizados += 1

            elif opcao == 3:
                print('\n------------------------------------------')
                print('---------------- EXTRATO -----------------')
                print('------------------------------------------')
                extrato_cash(vl_conta, hist_conta)
                print('------------------------------------------\n')

            elif opcao == 0:
                print('\nSaindo da sua conta!\n\n# # # # # # # # # # # # #')
                break

            else:
                print('\nValor digitado inválido!\n')

        except Exception as error:
            print(f'{error}')
