import pandas as pd
import numpy as np
from load import load_dim
from connect import connect_local_sql_server_2016, engine_local_sql_server_2016

# input extract paths
second_load_fact_path = "../source_data/update_procedure_cost.csv"
second_load_dim_diagnosis_path = "../source_data/update_dim_diagnosis.csv"
second_load_dim_procedure_path = "../source_data/update_dim_procedure.csv"
second_load_dim_facility_path = "../source_data/update_dim_facility.csv"


# get connection and engine
connection = connect_local_sql_server_2016()
engine = engine_local_sql_server_2016()





# mark obsolete dimensions as no longer active and set the end date
sqlScript = open('./update_dimensions.sql', 'r').read()

# execute each statement in the DDL script
for statement in sqlScript.split(";"):
    with connection.cursor() as cur:
        print(statement)
        cur.execute(statement)
# close the connection
connection.close()

# append updated dimension rows
update_dim_diagnosis = pd.read_csv(second_load_dim_diagnosis_path)
load_dim(update_dim_diagnosis, 'dim_Classifications_Diag', engine)

update_dim_procedure = pd.read_csv(second_load_dim_procedure_path)
load_dim(update_dim_procedure, 'dim_Classifications_Proc', engine)

update_dim_facility = pd.read_csv(second_load_dim_facility_path)
load_dim(update_dim_facility, 'dim_Facility', engine)


#  append new fact table rows

update_df = pd.read_csv(second_load_fact_path)
load_dim(update_df, 'fact_Procedure_Cost', engine)