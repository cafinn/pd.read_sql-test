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
# data = pd.read_sql(sql, master_connection, params=[])

master_cursor.execute(sql)
raw_data = master_cursor.fetchall()
print(f'{raw_data = }')
mod_data = [item[0] for item in raw_data]
print(f'{mod_data = }')
data = pd.DataFrame(raw_data)

# if 'TEST_PD' in data['name'].tolist():
if 'TEST_PD' in mod_data:
    print('Removing existing database...')
    print()
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

# ########################

sql = 'SELECT * FROM Parts'

data = pd.read_sql(sql, connection, params=[])
print(data)
print()

cursor.execute(sql)
print(f'{cursor.description = }')
print()
df_columns = [column[0] for column in cursor.description]
print(f'{df_columns = }')
print(f'{type(df_columns) = }')
print()
raw_data = cursor.fetchall()
print(f'{raw_data = }')
print()
mod_data = [list(row) for row in raw_data]
print(f'{mod_data = }')
print()
df = pd.DataFrame(mod_data, columns=df_columns)
print(df)
print()

# in compact form:

cursor.execute(sql)
df_columns = [column[0] for column in cursor.description]
raw_data = cursor.fetchall()
mod_data = [list(row) for row in raw_data]
df = pd.DataFrame(mod_data, columns=df_columns)
print(df)
print()


# ########################

cursor.close()
connection.close()

sql = 'DROP DATABASE TEST_PD'
master_cursor.execute(sql)

master_cursor.close()
master_connection.close()
