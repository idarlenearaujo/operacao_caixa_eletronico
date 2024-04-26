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
                
                else:
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

# Modificações no projeto v2 :mechanic:

Criar três novas funções: 

*   Cadastrar usuário (cliente do banco);
*   Cadastrar conta bancária (vincular com usuário);
*   Listar contas cadastradas.

Descrição:

*   O programa deve armazenar os usuários em uma lista, um usuário é composto por: nome, data de nascimento, cpf e endereço. O endereço é uma string com o formato: logradouro, nro - bairro - cidade/sigla - estado. Deve ser armazenado somente os números do CPF. Não podemos cadastrar 2 usuários com o mesmo CPF.

```
def cadastrar_cliente(clientes):

    cliente = {}

    cliente['cpf'] = input('\nDigite o CPF:')

    if not cpf_exists(cliente['cpf'], clientes):
        cliente['nome'] = input('\nDigite o nome: ')
        cliente['data_nascimento'] = input('\nDigite data de nascimento: ') 
        cliente['endereco'] = input('\nDigite o endereco [Rua, número - Bairro - Cidade - UF]: ')
    
        clientes.append(cliente)
        print('\nCliente Cadastrado!\n')

    else:
        print('\nCPF já cadastrado!!!\n')

```

*   O programa deve armazenar contas em uma lista, uma conta é composta por: agência, número da conta e usuário. O número da conta é sequencial, inicialmente em 1. O número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário.

```
def cadastrar_conta(num_conta, clientes):

    conta = {}
    
    cpf = input("\nDigite o CPF do cliente: ")
    
    if cpf_exists(cpf, clientes):

        conta['cpf'] = cpf
        conta['agencia'] = '0001'
        conta['numero_conta'] = num_conta
        
        contas.append(conta)

        print('\nConta Cadastrada!\n')
    
    else:
        print('\nCPF não cadastrado!')
```

*   Para vincular um usuário a uma conta, filtre a lista de usuários buscando o número do CPF informado para cada usuário da lista. Listar clientes e suas contas cadastradas no banco.

```
def listar_contas():
    print('\n-------------------------------------------')
    print('----------------- CONTAS ------------------')
    print('-------------------------------------------')
    for conta in contas:
        print(f"CPF: {conta['cpf']}, Número da Conta: {conta['numero_conta']}")
    print('-------------------------------------------\n')
```

```
def listar_clientes():  
    print('\n-------------------------------------------')
    print('---------------- CLIENTES -----------------')
    print('-------------------------------------------')
    for cliente in clientes:
        print(f"Nome: {cliente['nome']}, CPF: {cliente['cpf']}")
    print('-------------------------------------------\n')
```

# Modificações no projeto v3 :mechanic:

Estamos reformulando o projeto com a abordagem da Programação Orientada a Objetos (POO), que traz inúmeros benefícios, como a criação de softwares mais eficientes, organizados e sustentáveis.

Nesta atualização, realizamos as seguintes ações:
* Desenvolvemos novas classes;
* Implementamos novas funções;
* Estabelecemos relações entre as classes (através de herança simples, herança múltipla, encapsulamento e polimorfismo).

As classes criadas foram:

* Conta;
* Cliente;
* PessoaFisica;
* ContaCorrente;
* Historico;
* Transacao;
* Saque;
* Deposito.

Vale destacar que as classes PessoaFisica e ContaCorrente herdam instâncias e métodos das classes Cliente e Conta, respectivamente. Além disso, todas as transações (Deposito e Saque) são armazenadas no histórico de cada Conta pertencente ao respectivo Cliente.

Lembramos que, a cada ação executada no menu, ocorre uma verificação para confirmar se o cliente existe, se há uma conta associada a esse cliente, se há valor disponível para saque, se o número de operações não excedeu o limite e se o valor sacado é menor ou igual ao limite pré-estabelecido.

# Modificações no projeto v4 :mechanic:

Reformulado para acrescentar decoradores, iteradores e geradores.

* Decoradoes: São ferramentas poderosas usada para modificar o comportamento de uma função sem alterar seu código interno. Eles são aplicados usando @decorador acima da definição da função. Um decorador é uma função que recebe outra função como argumento.

```
def minha_funcao(func):
    def teste(*args, **kwargs):
        print("Imprimir esta mensagem")
    return teste

@minha_funcao
def sacar() [...]

```

* Geradores: São funções que retornam objetos ou itens percorríveis. Essas funções não produzem todos os itens de uma vez, mas eles os produzem conforme há a necessidade. Em suas funções o "return" é substituido por yield, que indica o retorno do next() do gerador criado.

```
def teste():
        for item in itens:
            if item >= 10:
                yield item
```

* Iteradores: São objetos iteradores que ultilizam os métodos __iter__() e __next__(). O método __iter__() retorna o próprio objeto iterador e o método __next__() retorna o próximo da sequência até que não haja mais itens e retorna a exceção StopIteration.

```
class iterador:
    def __init__(self):
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < 5:
            self.index += 1
        raise StopIteration
```

Usa-se os geradores para casos mais simples em que não haja complexidade no código e os iteradores para códigos mais robustos.

# Modificações no projeto v5 :mechanic:

Armazenando em um arquivo txt os valores informados.