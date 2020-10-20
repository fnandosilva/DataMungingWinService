import pyodbc
import databaseconnection
import pandas as pd

"""This is the library made to connect to my Sql database.
   The methods created in this library comtemplates the CRUD,
   but only the create were built. 
"""

server = 'Insert a valid SQL Server here'
database = 'Insert a valid SQL Database here'
username = 'Insert a valid Username here'
password = 'Insert a valid password here'

def create_sql_connection():
    print("Opening the SQL database conection")
    conn = pyodbc.connect('Driver={SQL Server};Server='+server+';Database='+database+';UID='+username+';PWD='+password)
    cursor = conn.cursor()
    return cursor
    
def insert_into_table_CustomersPurchase(dataframe):
    print("Inserting data into table CustomersPurchase")
    sql_connection = create_sql_connection()
    for index, row in dataframe.iterrows():
        sql_connection.execute("insert into CustomersPurchase(CPF, Private, Incompleto, DataUltimaCompra, TicketMedio, TicketUltimaCompra, LojaMaisFrequente, LojaUltimaCompra) values(?,?,?,?,?,?,?,?)", 
                               row.CPF, row.Private, row.Incompleto, row.DataUltimaCompra, row.TicketMedio, row.TicketUltimaCompra, row.LojaMaisFrequente, row.LojaUltimaCompra)
    sql_connection.commit()
    sql_connection.close()

def create_table_CustomersPurchase():
    print("Creating the table CustomersPurchase if not exists")
    sql_connection = create_sql_connection()
    sql_connection.execute("if OBJECT_ID('CustomersPurchase') IS NULL CREATE TABLE [dbo].CustomersPurchase (CPF nvarchar(18), Private bit," + 
                           " Incompleto bit, DataUltimaCompra date, TicketMedio nvarchar(100), TicketUltimaCompra nvarchar(100) null," +
                           " LojaMaisFrequente nvarchar(18) null, LojaUltimaCompra nvarchar(18) null);")
    sql_connection.commit()




