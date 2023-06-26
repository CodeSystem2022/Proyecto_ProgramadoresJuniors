import psycopg2


class Transaction:
    def __init__(self, client, account, network, bank, amount, date, transaction_type):
        self.id = 1
        self.client = client
        self.account = account
        self.network = network
        self.bank = bank
        self.amount = amount
        self.date = date
        self.transaction_type = transaction_type

    def execute(self):
        if self.transaction_type == "deposit":
            self.deposit()
        elif self.transaction_type == "withdraw":
            self.withdraw()
        elif self.transaction_type == "transfer":
            self.transfer()

    def deposit(self):
        self.account.deposit(self.amount)
        self.save_transaction_to_database()

    def withdraw(self):
        self.account.withdraw(self.amount)
        self.save_transaction_to_database()

    def transfer(self):
        target_account = self.prompt_target_account()
        if target_account:
            self.account.transfer(self.amount, target_account)
            self.save_transaction_to_database()
        else:
            print("Invalid target account.")

    def save_transaction_to_database(self):
        conn = psycopg2.connect(
            database="BankApp",
            user="postgres",
            password="554585",
            host="127.0.0.1",
            port="5432",
        )

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions (client_id, account_id, transactions_network_id, bank_id, amount, date, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                self.client.id,
                self.account.id,
                self.network.id,
                self.bank.id,
                self.amount,
                self.date,
                self.transaction_type,
            ),
        )
        conn.commit()
        conn.close()
