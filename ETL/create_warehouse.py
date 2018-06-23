import getpass
import pyodbc

def create():
    # get connection to local SQL Server 2016 database
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-RD37B89\SQLEXPRESS;"
                          "Database=HealthcareCostWarehouse;"
                          "Trusted_Connection=yes;")

    # read SQL create DDL Script
    sqlScript = open('./create.sql', 'r').read()

    # execute each statement in the DDL script
    for statement in sqlScript.split(";"):
        with cnxn.cursor() as cur:
            print('running: ' + statement)
            cur.execute(statement)

    # close the connection
    cnxn.close()

    print('done running create script!')
    return