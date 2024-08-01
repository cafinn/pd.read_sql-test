# pd.read_sql test
 
A minimum reproducible example to demonstrate the following warning occorring with MS SQL Express Server 15.0.4249 (also MS SQL Server 14.0.2042.3), Python 3.10.7, Pandas 1.5.0:

>UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy. return pd.read_sql(sql, self.connection, params=[search_term, not_search_term])

Using pd.read_sql is the recommended method for creating a pandas dataframe from an sql query in python 

ref https://learn.microsoft.com/en-us/sql/machine-learning/data-exploration/python-dataframe-pandas?view=sql-server-ver16

work_around.py has a method just using cursor that avoids the warning
