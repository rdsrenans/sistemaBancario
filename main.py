import cmd
import os
import sys
from datetime import datetime as dt


class Account:
    balance = 0.0
    number_of_withdrawals = 0
    LIMIT_WITHDRAWALS = 3
    LIMIT = 500
    statement = {}


def start():

    while True:

        operation = int(input(show_menu()))

        match operation:
            case 1:
                draw()

            case 2:
                deposit()

            case 3:
                show_extract()

            case 4:
                print('\tObrigado pela preferencia!')
                sys.exit()

            case _:
                print('\tOperação inválida, escolha uma da lista!')


def show_menu() -> str:
    menu = '''
            Olá, o que você deseja fazer?

            1 - Sacar
            2 - Depositar
            3 - Extrato
            4 - Sair

        '''
    return menu


def draw():
    cls()
    is_limit = True
    while is_limit:
        value = float(input('\tQual valor deseja sacar?\n'))
        cls()

        if value <= Account.balance:
            if value <= Account.LIMIT:
                if Account.number_of_withdrawals < Account.LIMIT_WITHDRAWALS:
                    current_time = dt.now()
                    Account.statement.update({current_time: ['Saque: R$', value]})
                    Account.balance -= value
                    show_balance()
                    Account.number_of_withdrawals += 1
                    is_limit = False
                else:
                    print("\tNúmero de saques diário excedido!")
                    break
            else:
                print(f'\tLimite de R$ {Account.LIMIT} por saque, escolher valor menor.')
        else:
            print('\tSaldo insuficiente!')
            show_balance()
            is_limit = False


def deposit():
    cls()
    value = float(input('\tQual valor deseja depositar?\n'))
    cls()
    current_time = dt.now()
    Account.statement.update({current_time: ['Deposito: R$', value]})
    Account.balance += value
    show_balance()


def show_extract():
    cls()
    if len(Account.statement) == 0:
        print('\tNão foram realizadas movimentações.')
    else:
        for x, y in Account.statement.items():
            print(x.strftime('\t%d/%m/%Y as %H:%M:%S'), '\n\t', y[0], f'{y[1]:.2f}\n')
        show_balance()


def show_balance() -> None:
    print(f'\tSeu saldo é de R$ {Account.balance:.2f}\n')


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    start()
