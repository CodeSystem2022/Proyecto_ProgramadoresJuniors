# -*- coding: utf-8 -*-

from datetime import datetime
from accounts import Account
from Transaction import Transaction
from Clients import Client
from Banks import Bank
from TransactionNetwork import TransactionNetwork
import psycopg2

conn = psycopg2.connect(
    database="BankApp",
    user="postgres",
    password="554585",
    host="127.0.0.1",
    port="5432",
)

cursor = conn.cursor()

# Obtener datos de los bancos desde la base de datos
cursor.execute("SELECT id, name, network_type_id FROM banks")
bank_records = cursor.fetchall()
banks = []

for bank_record in bank_records:
    bank_id, bank_name, network_type_id = bank_record

    # Obtener el tipo de red según el ID de la red en la base de datos
    cursor.execute(
        "SELECT network_type FROM transactions_networks WHERE id = %s",
        (network_type_id,),
    )
    network_type = cursor.fetchone()[0]

    # Crear objeto Bank y agregarlo a la lista de bancos
    bank = Bank(bank_name, network_type)
    banks.append(bank)


# Cerrar la conexión a la base de datos
conn.close()

# Crear objetos Client, Account, TransactionNetwork y Bank según sea necesario
client = Client("John Doe", "Las Vegas 254", "15458005", "Banco Ciudad de Buenos Aires")
account = Account("1234567890", 554832586, 1000.00)
transaction_network = TransactionNetwork("Red Link", "Red de transacciones de link")

# Utilizar los objetos Bank creados desde la base de datos
bank = banks[0]

# Crear un objeto Transaction
transaction = Transaction(
    client, account, transaction_network, bank, 500.00, datetime.now(), "deposit"
)

# Ejecutar la transacción
transaction.execute()

# Obtener información de la transacción
print("Transaction Information:")
print(f"Client: {transaction.client.name}")
print(f"Account Number: {transaction.account.account_number}")
print(f"Network: {transaction.network.network_type}")
print(f"Bank: {transaction.bank.name}")
print(f"Amount: {transaction.amount}")
print(f"Date: {transaction.date}")
print(f"Type: {transaction.transaction_type}")
print(f"Balance: {transaction.account.balance}")
