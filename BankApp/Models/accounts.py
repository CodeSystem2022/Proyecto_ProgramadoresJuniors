class Account:
    def __init__(self, client, account_number, balance):
        self.id = 1
        self.client = client
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def transfer(self, amount, target_account):
        self.balance -= amount
        target_account.balance += amount