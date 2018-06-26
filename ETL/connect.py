import os
import pyodbc
import sqlalchemy
import urllib

def connect_local_sql_server_2016():

    #constring = "Driver={SQL Server Native Client 11.0};" +\
    #                      "Server=" + os.environ['SERVER'] + ";" +\
    #                      "Database=" + os.environ['DB_NAME'] + ";" +\
    #                      "trusted_connection=yes;"
    constring = (
        r'Driver={SQL Server};'
        r'Server=' + os.environ['SERVER'] + ';'
        r'Database=' + os.environ['DB_NAME'] + ';'
        r'Trusted_Connection=yes;'
    )
    connection = pyodbc.connect(constring)


    return connection

def engine_local_sql_server_2016():
    params = urllib.parse.quote_plus(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RD37B89\SQLEXPRESS;DATABASE=HealthcareCostWarehouse;Trusted_Connection=yes')
    #constring = "mssql+pyodbc://" + os.environ['SERVER'] + "/" + os.environ['DB_NAME'] + "?trusted_connection=yes?driver=SQL+Server+Native+Client+11.0"
    constring = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    #pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server=os.environ['SERVER'], database = 'SDE')
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