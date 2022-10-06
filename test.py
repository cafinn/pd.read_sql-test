from pyodbc import connect as pyodbc_connect

import pandas as pd


# Uses a local installation of "SQL Server 2019 Express Edition"
# - Basic installation
#
# MS SQL Server Management Studio notes for diagnostic access:
#   click connect icon
#   under server name, click browse for more...
#   expand the database engine +
#   select <local machine name>\SQLEXPRESS
#   Use Windows Authentication

connection_string = 'Driver={SQL Server};Server=localhost\\SQLEXPRESS;'
connection_string += 'Database=master;Trusted_Connection=True;'

# print(f'{connection_string = }')

master_connection = pyodbc_connect(connection_string, autocommit=True)
master_cursor = master_connection.cursor()

# Delete TEST_PD if it exists
sql = 'SELECT name FROM master.dbo.sysdatabases'
data = pd.read_sql(sql, master_connection, params=[])

if 'TEST_PD' in data['name'].tolist():
    print('Removing existing database...')
    sql = 'DROP DATABASE TEST_PD'
    master_cursor.execute(sql)

sql = 'CREATE DATABASE TEST_PD'
master_cursor.execute(sql)

# open production connection without autocommit
connection = pyodbc_connect(connection_string)
cursor = connection.cursor()

sql = 'USE TEST_PD'
cursor.execute(sql)
connection.commit()

# Populate some data

sql = """
CREATE TABLE Parts(
[impPartID] NVARCHAR(30) NOT NULL,
[impRowVersion] TIMESTAMP NULL
);

INSERT INTO Parts (impPartID) VALUES ('ADE012345');
INSERT INTO Parts (impPartID) VALUES ('ADE012346');
INSERT INTO Parts (impPartID) VALUES ('ADE012347');
INSERT INTO Parts (impPartID) VALUES ('ADE012348');
INSERT INTO Parts (impPartID) VALUES ('ADE012349');
"""
cursor.execute(sql)
connection.commit()

sql = 'SELECT * FROM Parts'
data = pd.read_sql(sql, connection, params=[])
print(data)
print()


cursor.close()
connection.close()

sql = 'DROP DATABASE TEST_PD'
master_cursor.execute(sql)

master_cursor.close()
master_connection.close()
