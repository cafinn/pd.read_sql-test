# pd.read_sql test
 
creating a minimum reproducable example to demonstrate the following warning:

UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy.
return pd.read_sql(sql, self.connection, params=[search_term, not_search_term])

using pd.read_sql is the recommended method for creating a pandas dataframe from an sql query in python 

ref https://learn.microsoft.com/en-us/sql/machine-learning/data-exploration/python-dataframe-pandas?view=sql-server-ver16