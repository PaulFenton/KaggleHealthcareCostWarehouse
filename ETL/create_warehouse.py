import pyodbc
import os


def create(connection):
    print('running warehouse creation ddl scripts..')

    # read SQL create DDL Script
    sqlScript = open('./create.sql', 'r').read()

    # execute each statement in the DDL script
    for statement in sqlScript.split(";"):
        with connection.cursor() as cur:
            cur.execute(statement)

    # close the connection
    connection.close()

    print('done!')
    return