import os
import sys
import bank
import time
import textwrap


def client_filter(clients):
    cpf = input("\n\tInforme o CPF do cliente: \n\t")
    cls()
    filtered_client = [client for client in clients if client.cpf == cpf]
    return filtered_client[0] if filtered_client else None


def client_verify(clients):
    client = client_filter(clients)

    if not client:
        print('\n\tAinda não é cliente!')
        time.sleep(3)
        cls()
        return

    return client


def recover_client_account(client):
    if not client.accounts:
        print('\n\tCliente não possui conta!')

    return client.accounts[0]


def deposit(clients):
    cls()
    movement(clients, text_transaction='depositar', transaction='deposit')


def withdrawal(clients):
    movement(clients, text_transaction='sacado', transaction='withdrawal')


def movement(clients, /, text_transaction, transaction):
    client = client_verify(clients)
    if client is None: return

    transaction_action = 'empty'

    value = float(input(f'\n\tInforme o valor a ser {text_transaction}: '))
    if transaction == 'deposit':
        transaction_action = bank.Deposit(value)
    elif transaction == 'withdrawal':
        transaction_action = bank.Withdrawal(value)

    account = recover_client_account(client)
    if not account:
        return

    client.transaction_action(account, transaction_action)


def show_extract(clients):
    client = client_verify(clients)
    if client is None: return

    account = recover_client_account(client)
    if not account: return

    print("\n-----------------Extrato---------------------")
    transactions = account.statement.transactions

    extract = ''
    if not transactions:
        extract = '\n\tNão foram realizadas movimentações.'
    else:
        for transaction in transactions:
            extract += f'\n{transaction["Tipo"]}:\n\tR${transaction["Valor"]:.2f}'

    print(extract)
    print(f'\n\tSeu saldo é de R$ {account.balance:.2f}\n')
    print("---------------------------------------")


def new_client(clients):
    client = client_verify(clients)

    if client:
        print('CPF já cadastrado')
        return

    cpf = input('\n\tInforme novamente o CPF: ')
    name = input('\tInforme o nome completo do usuário: ')
    birthday = input('\tInforme da data de nascimento (dd-mm-aaaa): ')
    address = input('\tInforme o endereço (logradouro, nro - bairro - cidade/sigla estado): ')

    client = bank.RegularAccount(name=name, birthday=birthday, cpf=cpf, address=address)

    clients.append(client)

    print("Usuário criado com sucesso!")


def new_account(account_number, clients, accounts):
    client = client_verify(clients)
    if client is None: return

    client = client_filter(clients)

    account = bank.CheckingAccount.new_account(client=client, account_number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    print(f'\n\tContra cadastrada para cliente!')


def accounts_list(accounts):

    if not accounts:
        print("\n\n\tNão existe contas\n\n")
        time.sleep(4)
        cls()
        return

    for account in accounts:
        print("-" * 70)
        print(textwrap.dedent(str(account)))


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu() -> str:
    menu = '''
        Olá, escolha o numero da operação que deseja!

        1 - Sacar
        2 - Depositar
        3 - Extrato
        4 - Novo Cliente
        5 - Nova conta
        6 - Listar contas
        7 - Sair

        Operação: '''
    return menu


def start():
    clients = []
    accounts = []

    while True:
        operation = 0
        try:
            operation = int(input(show_menu()))
        except ValueError:
            print('\n\t\t\tSomente números podem ser digitados!')

        match operation:
            case 1:
                cls()
                withdrawal(clients)

            case 2:
                cls()
                deposit(clients)

            case 3:
                cls()
                show_extract(clients)

            case 4:
                cls()
                new_client(clients)

            case 5:
                cls()
                account_number = len(accounts) + 1
                new_account(account_number, clients, accounts)

            case 6:
                cls()
                accounts_list(accounts)

            case 7:
                cls()
                print('\t\t\tObrigado pela preferencia!')
                sys.exit()

            case _:
                cls()
                print('\t\t\tOperação inválida, escolha uma da lista!')


start()
