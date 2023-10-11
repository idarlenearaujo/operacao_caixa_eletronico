# Desafio DIO: Operação Caixa Eletrônico :woman_technologist:

Projeto em Python - Diretrizes Fundamentais:

*	**Depósito:** :moneybag: Deve ser possível depositar valores positivos para uma conta bancária. A V1 (versão 1) do projeto trabalha apenas com 1 usuário, dessa forma não precisamos nos preocupar em identificar qual é o número da agência e conta bancária. Todos os depósitos devem ser armazenados em uma variável e exibidos na operação de extrato.

```
def depositar_cash(valor_conta): 
    
    try:
        valor_deposito = float(input("\nDigite o valor que deseja depositar: ")) 

        if valor_deposito > 0: 
            return valor_deposito
    
    except:
        print('\nENTRADA INVÁLIDA!!!\nValor esperado: > 0.00\nInforme um valor válido.')
```

*	**Saque:** :money_with_wings: O sistema deve permitir realizar 3 saques diários com limite máximo de R$ 500,00 por saque. Caso o usuário não tenha saldo em conta, o sistema deve exibir uma mesnagem informando que não será possível sacar o dinheiro por falta de saldo. Todos os saques devem ser armazenados em uma variável e exibidos na operação de extrato.

 ```
 def sacar_cash(valor_conta, saques_realizados): 
    
    if saques_realizados < 3:
        
        try:
            valor_saque = float(input("\nDigite o valor que deseja sacar: ")) 

            if 0 < valor_saque <= 500:
                if valor_conta >= valor_saque:
                    return valor_saque 
                
                print("\nSALDO INSUFICIENTE!!!") 
            
            else:
                print('\nO valor informado não deve ser zero, valor negativo ou superior a R$ 500.00.\nInforme um valor válido.')
        
        except:
            print('Valor inválido informado.)
    
    else:
        print('Você atingiu o limite de 3 saques')                                                                                                                     
    return 0 
 ```

*	**Extrato:** :memo: Essa operação deve listar todos os depósitos e saques realizados na conta. No fim da listagem deve ser exibido o saldo atual da conta. Os valores devem ser exibidos utilizando o formato R$ xxx.xx, exmplo: 1500.45 = R$ 1500.45

```
def extrato_cash(valor_conta, historico_conta): 

    for dados in historico_conta:
        print(dados)

    print(f"\nValor em conta atualizado: R$ {valor_conta:.2f}")
```
