import sys
from datetime import datetime as dt


class Account:
    saldo = 0.0
    LIMITE = 500
    historico = {}
    numero_saques = 0
    LIMITE_SAQUES = 3


def start():

    while True:

        operacao = int(input(imprime_menu()))

        match operacao:
            case 1:
                sacar()

            case 2:
                depositar()

            case 3:
                imprimir_extrato()

            case 4:
                print('Obrigado pela preferencia!')
                sys.exit()

            case _:
                print('Operação inválida, escolha uma da lista!')


def imprime_menu() -> str:
    menu = '''
            Olá, o que você deseja fazer?

            1 - Sacar
            2 - Depositar
            3 - Extrato
            4 - Sair

        '''
    return menu


def sacar():
    dentro_limite = True
    while dentro_limite:
        valor = float(input('Qual valor deseja sacar?\n'))

        if valor <= Account.saldo:
            if valor <= Account.LIMITE:
                if Account.numero_saques < Account.LIMITE_SAQUES:
                    current_time = dt.now()
                    Account.historico.update({current_time: ['Saque: R$', valor]})
                    Account.saldo -= valor
                    imprimir_saldo()
                    Account.numero_saques += 1
                    dentro_limite = False
                else:
                    print("Número de saques diário excedido!")
                    break
            else:
                print(f'Limite de R$ {Account.LIMITE} por saque, escolher valor menor.')
        else:
            print('Saldo insuficiente!')
            imprimir_saldo()
            dentro_limite = False


def depositar():
    valor = float(input('Qual valor deseja depositar?\n'))
    current_time = dt.now()
    Account.historico.update({current_time: ['Deposito: R$', valor]})
    Account.saldo += valor
    imprimir_saldo()


def imprimir_extrato():
    for x, y in Account.historico.items():
        print(x.strftime('%d/%m/%Y as %H:%M:%S'), '-', y[0], f'{y[1]:.2f}')
    imprimir_saldo()


def imprimir_saldo() -> None:
    print(f'Seu saldo é de R$ {Account.saldo:.2f}')


if __name__ == '__main__':
    start()
