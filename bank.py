from datetime import datetime as dt
from abc import ABC, abstractmethod


class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def transaction_action(self, account, transaction):
        transaction.record(account)

    def add_account(self, account):
        self.accounts.append(account)


class RegularAccount(Client):
    def __init__(self, name, birthday, cpf, address):
        super().__init__(address)
        self.name = name
        self.birthday = birthday
        self.cpf = cpf


class Account:
    def __init__(self, account_number, client):
        self._balance = 0
        self._account_number = account_number
        self._agency = "0001"
        self._client = client
        self._statement = Statement()

    @classmethod
    def new_account(cls, client, account_number):
        return cls(account_number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def statement(self):
        return self._statement

    def withdrawal(self, value):
        if self.balance > value:
            self._balance -= value
            return True
        return False

    def deposit(self, value):
        if value > 0:
            self._balance += value
            return True
        return False


class CheckingAccount(Account):
    def __init__(self, account_number, client, limit_value_withdrawals=500, limit_withdrawals=3):
        super().__init__(account_number, client)
        self.limit_draw = limit_value_withdrawals
        self.limit_withdrawals = limit_withdrawals

    def withdrawal(self, value):
        number_of_withdrawals = len(
            [transaction for transaction in self.statement.transactions if transaction["Tipo"] == "Saque"])
        limit_value_exceeded = value > self.limit_draw
        limit_withdrawals_exceeded = number_of_withdrawals >= self.limit_withdrawals

        if limit_value_exceeded:
            print(f'\tLimite de R$ {self.limit_draw} por saque, escolher valor menor.')

        elif limit_withdrawals_exceeded:
            print("\tNúmero de saques diário excedido!")

        else:
            return super().withdrawal(value)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agency}
            C/C:\t\t{self.account_number}
            Titular:\t{self.client.name}
        """


class Statement:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction, transaction_type='deposit'):
        self._transactions.append(
            {
                'Tipo': 'Saque' if transaction_type == 'drawn' else 'Deposito',
                'Valor': transaction.value,
                'Data': dt.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @classmethod
    @abstractmethod
    def record(cls, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def record(self, account):
        transaction_success = account.withdrawal(self._value)
        if transaction_success:
            account.statement.add_transaction(self, transaction_type='drawn')


class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def record(self, account):
        transaction_success = account.deposit(self._value)
        if transaction_success:
            account.statement.add_transaction(self)
