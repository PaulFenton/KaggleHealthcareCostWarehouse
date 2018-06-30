import os
import pyodbc
import sqlalchemy
import urllib

def connect_local_sql_server_2016():

    constring = (
        r'Driver={SQL Server};'
        r'Server=' + os.environ['SERVER'] + ';'
        r'Database=' + os.environ['DB_NAME'] + ';'
        r'Trusted_Connection=yes;'
    )
    connection = pyodbc.connect(constring)


    return connection

def engine_local_sql_server_2016():
    params = urllib.parse.quote_plus(r'DRIVER={SQL Server Native Client 11.0};' + os.environ['SERVER'] + ';DATABASE=' + os.environ['DB_NAME'] + ';Trusted_Connection=yes')
    constring = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    engine = sqlalchemy.create_engine(constring)
    return engine

def connect_remote_sql_server_2016():
    constring = "Driver={SQL Server Native Client 11.0};" + \
                "Server=" + os.environ['SERVER'] + ";" + \
                "Database=" + os.environ['DB_NAME'] + ";" + \
                "UID=" + os.environ['DB_USER'] + ";" + \
                "PWD=" + os.environ['DB_PASSWORD'] + ";"
    connection = pyodbc.connect(constring)

    return connection
