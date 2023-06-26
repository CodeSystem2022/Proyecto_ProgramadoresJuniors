# -*- coding: utf-8 -*-

import psycopg2
import random


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
    CREATE TABLE transactions_networks (
        id SERIAL PRIMARY KEY,
        network_type VARCHAR(20),
        description VARCHAR(200)
    )
"""
)


cursor.execute(
    """
    INSERT INTO transactions_networks (network_type, description)
    VALUES
        ('Red Link', 'Red de transacciones link '),
        ('Banelco', 'Red de transacciones banelco')
"""
)

cursor.execute(
    """
    CREATE TABLE banks (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        network_type_id INTEGER,
        FOREIGN KEY (network_type_id) REFERENCES transactions_networks (id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE clients (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        address VARCHAR(200),
        phone VARCHAR(15),
        bank_id INTEGER,
        FOREIGN KEY (bank_id) REFERENCES banks (id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE accounts (
        id SERIAL PRIMARY KEY,
        client_id INTEGER,
        account_number VARCHAR(20),
        balance DECIMAL(10, 2),
        bank_id INTEGER,
        FOREIGN KEY (bank_id) REFERENCES banks (id),
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE transactions(
        id SERIAL PRIMARY KEY,
        client_id INTEGER,
        account_id INTEGER,
        transactions_network_id INTEGER,
        bank_id INTEGER,
        amount DECIMAL(10, 2),
        date TIMESTAMP,
        type VARCHAR(20),
        FOREIGN KEY (client_id) REFERENCES clients (id),
        FOREIGN KEY (account_id) REFERENCES accounts (id),
        FOREIGN KEY (transactions_network_id) REFERENCES transactions_networks (id),
        FOREIGN KEY (bank_id) REFERENCES banks (id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE link (
        id SERIAL PRIMARY KEY,
        transactions_network_id INTEGER,
        banks VARCHAR(50),
        FOREIGN KEY (transactions_network_id) REFERENCES transactions_networks (id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE banelco (
        id SERIAL PRIMARY KEY,
        transactions_network_id INTEGER,
        banks VARCHAR(50),
        FOREIGN KEY (transactions_network_id) REFERENCES transactions_networks (id)
    )
"""
)


cursor.execute(
    """
    CREATE TABLE network_banks (
        network_id INTEGER,
        bank_id INTEGER,
        FOREIGN KEY (network_id) REFERENCES transactions_networks (id),
        FOREIGN KEY (bank_id) REFERENCES banks (id),
        PRIMARY KEY (network_id, bank_id)
    )
"""
)


# ----------------------------------------------------------------------------
#                            FIRST QUERY
# banks using link network
link_banks = [
    "Banco Bica",
    "Banco Ciudad de Buenos Aires",
    "Banco CMF",
    "Banco Coinag",
    "Banco Credicoop Coop. Ltda.",
    "Banco de Comercio",
    "Banco de Corrientes",
    "Banco Columbia",
    "Banco de Formosa",
    "Banco de la Nacion Argentina",
    "Banco de La Pampa",
    "Banco de la Provincia de Buenos Aires",
    "Banco de la Provincia de Cordoba",
    "Banco del Chubut",
    "Banco Dino",
    "Banco Entre Rios",
    "Banco Hipotecario",
    "Banco Industrial",
    "Banco Interfinanzas",
    "Banco Mariva",
    "Banco Masventas",
    "Banco Meridian",
    "Banco Municipal",
    "Banco Piano",
    "Banco Provincia del Neuquen",
    "Banco Rioja",
    "Banco Roela",
    "Banco Saenz",
    "Banco San Juan",
    "Banco Santa Cruz",
    "Banco Santa Fe",
    "Banco Santiago del Estero",
    "Banco Tierra del Fuego",
    "Credito Regional Cia. Financiera",
    "Efectivo Si",
    "Montemar Cia. Financiera",
    "Nuevo Banco del Chaco",
]

for bank_name in link_banks:
    cursor.execute(
        """
        INSERT INTO banks (name, network_type_id)
        VALUES ('{}', 1)
        """.format(
            bank_name
        )
    )


cursor.execute("SELECT id FROM transactions_networks WHERE network_type = 'Red Link'")
link_network_id = cursor.fetchone()[0]


for bank_name in link_banks:
    cursor.execute(
        """
        INSERT INTO link (transactions_network_id, banks)
        VALUES (%s, %s)
        """,
        (link_network_id, bank_name),
    )

# banks using banelco network
banelco_banks = [
    "Banco de Galicia y Buenos Aires 3",
    "Banco BBVA Frances",
    "Banco Santander Rio",
    "Banco Macro",
    "Banco Brubank",
    "Banco HSBC",
    "Banco ICBC",
    "Banco Patagonia",
    "Banco Itau",
    "Banco Supervielle",
    "Rebanking (.reba)",
    "Banco Comafi",
    "Banco del Sol",
]


for bank_name in banelco_banks:
    cursor.execute(
        """
        INSERT INTO banks (name, network_type_id)
        VALUES ('{}', 2)
        """.format(
            bank_name
        )
    )

cursor.execute("SELECT id FROM transactions_networks WHERE network_type = 'Banelco'")
banelco_network_id = cursor.fetchone()[0]


for bank_name in banelco_banks:
    cursor.execute(
        """
        INSERT INTO banelco (transactions_network_id, banks)
        VALUES (%s, %s)
        """,
        (banelco_network_id, bank_name),
    )


# first client
cursor.execute(
    """
    INSERT INTO clients (id, name, address, phone, bank_id)
    VALUES (1, 'Soel', 'El Moro 315', '2604306032', 5)
    """
)

# first account
account_number = str(random.randint(1000000000, 9999999999))  # random account number
cursor.execute(
    """
    INSERT INTO accounts (id, client_id, account_number, balance, bank_id)
    VALUES (1, 1, '{}', 100000.00, 5)
    """.format(
        account_number
    )
)

# now we gonna do our first transaction and then we gonna show the final table result
transaction_id = random.randint(1, 1000)  # random transaction id
cursor.execute(
    """
    INSERT INTO transactions (id, client_id, account_id, transactions_network_id, bank_id, amount, date, type)
    VALUES ({}, 1, 1, 1, 5, 1500.00, NOW(), 'extraction')
    """.format(
        transaction_id
    )
)

conn.commit()
conn.close()
