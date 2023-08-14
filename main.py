import os
import sys
from datetime import datetime as dt


def start():
    balance = 0.0
    number_of_withdrawals = 0
    LIMIT_WITHDRAWALS = 3
    LIMIT = 500
    BANK_AGENCY = '0001'
    statement = {}
    users = []
    accounts = []

    while True:

        operation = int(input(show_menu()))

        match operation:
            case 1:
                balance, \
                    number_of_withdrawals, \
                    statement = draw(balance=balance,
                                     limit_draw=LIMIT,
                                     number_of_withdrawals=number_of_withdrawals,
                                     limit_withdrawals=LIMIT_WITHDRAWALS,
                                     statement=statement)

            case 2:
                balance, statement = deposit(statement, balance)

            case 3:
                show_extract(balance, statement=statement)

            case 4:
                new_user(users)

            case 5:
                account_number = len(accounts)
                account = new_account(BANK_AGENCY, account_number, users)

                if account:
                    accounts.append(account)

            case 6:
                accounts_list(accounts)

            case 7:
                print('\tObrigado pela preferencia!')
                sys.exit()

            case _:
                print('\tOperação inválida, escolha uma da lista!')


def show_menu() -> str:
    menu = '''
            Olá, escolha o numero da operação que deseja!

            1 - Sacar
            2 - Depositar
            3 - Extrato
            4 - Novo usuário
            5 - Nova conta
            6 - Listar contas            
            7 - Sair

        '''
    return menu


def draw(*, balance, limit_draw, number_of_withdrawals, limit_withdrawals, statement):
    cls()
    is_limit = True
    while is_limit:
        value = float(input('\tQual valor deseja sacar?\n'))
        cls()

        if value <= balance:
            if value <= limit_draw:
                if number_of_withdrawals < limit_withdrawals:
                    current_time = dt.now()
                    statement.update({current_time: ['Saque: R$', value]})
                    balance -= value
                    show_balance(balance)
                    number_of_withdrawals += 1
                    is_limit = False
                else:
                    print("\tNúmero de saques diário excedido!")
                    break
            else:
                print(f'\tLimite de R$ {limit_draw} por saque, escolher valor menor.')
        else:
            print('\tSaldo insuficiente!')
            show_balance(balance)
            is_limit = False

    return balance, number_of_withdrawals, statement


def deposit(statement, balance, /):
    cls()
    value = float(input('\tQual valor deseja depositar?\n'))
    cls()
    current_time = dt.now()
    statement.update({current_time: ['Deposito: R$', value]})
    balance += value
    show_balance(balance)
    return balance, statement


def show_extract(balance, *, /, statement):
    cls()
    if len(statement) == 0:
        print('\tNão foram realizadas movimentações.')
    else:
        for x, y in statement.items():
            print(x.strftime('\t%d/%m/%Y as %H:%M:%S'), '\n\t', y[0], f'{y[1]:.2f}\n')
            print(f'\tSeu saldo é de R$ {balance:.2f}\n')


def show_balance(balance) -> None:
    print(f'\tSeu saldo é de R$ {balance:.2f}\n')


def new_user(users):
    cpf = input("Informe o CPF (somente números): )")
    user = user_filter(cpf, users)

    if user:
        print(f'CPF já cadastrado para: {user["name"]}')
        return

    name = input('Informe o nome completo do usuário: ')
    birthday = input('Informe da data de nascimento (dd-mm-aaaa): ')
    address = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ')

    users.append({'name': name, 'birthday': birthday, 'cpf': cpf, 'address': address})

    print("Usuário criado com sucesso!")


def user_filter(cpf, users):
    filtered_users = [user for user in users if users['cpf'] == cpf]
    return filtered_users[0] if filtered_users else None


def new_account(bank_agency, account_number, users):
    cpf = input('Informe o número do CPF: ')
    user = user_filter(cpf, users)

    if user:
        print('Conta criada com sucesso!')
        return {'bank_agency': bank_agency, 'account_number': account_number, 'user': user}

    print('Usuário não encontrado!')


def accounts_list(accounts):
    for account in accounts:
        print(f'Agência: {account["bank_agency"]},'
              f'C/C: {account["account_number"]},'
              f'Titular: {account["name"]}')


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    start()
