import sys
from datetime import datetime as dt

menu = '''
    Olá, o que você deseja fazer?
    
    1 - Sacar
    2 - Depositar
    3 - Extrato
    4 - Sair

'''

saldo = 0.0
LIMITE = 500
historico = {}
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    operacao = int(input(menu))

    match operacao:
        case 1:
            dentro_limite = True
            while dentro_limite:
                valor = float(input('Qual valor deseja sacar?\n'))

                if valor <= saldo: # TODO: Adicionar metodo de limite de saque diario
                    if valor <= LIMITE:
                        current_time = dt.now()
                        historico.update({current_time: ['Saque: R$', valor]})
                        saldo -= valor
                        print(f'Seu novo saldo é R$ {saldo:.2f}')
                        dentro_limite = False
                    else:
                        print(f'Limite de R$ {LIMITE} por saque, escolher valor menor.')
                else:
                    print('Saldo insuficiente!')
                    print(f'Seu saldo é R$ {saldo:.2f}')
                    dentro_limite = False

        case 2:
            valor = float(input('Qual valor deseja depositar?\n'))
            current_time = dt.now()
            historico.update({current_time: ['Deposito: R$', valor]})
            saldo += valor
            print(f'Seu novo saldo é R$ {saldo:.2f}')

        case 3:
            for x, y in historico.items():
                print(x.strftime('%d/%m/%Y as %H:%M:%S'), '-', y[0], f'{y[1]:.2f}')
            print(f'Seu saldo é R$ {saldo:.2f}')
        case 4:
            print('Obrigado pela preferencia!')
            sys.exit()

        case _:
            print('Operação inválida, escolha uma da lista!')