import os
import pyodbc
import sqlalchemy

def connect_local_sql_server_2016():

    constring = "Driver={SQL Server Native Client 11.0};" +\
                          "Server=" + os.environ['SERVER'] + ";" +\
                          "Database=" + os.environ['DB_NAME'] + ";" +\
                          "trusted_connection=yes;"
    connection = pyodbc.connect(constring)


    return connection

def engine_local_sql_server_2016():
    constring = "mssql+pyodbc://" + os.environ['SERVER'] + "/" + os.environ['DB_NAME'] + "?trusted_connection=yes"
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