from extract import read_source_file, extract_dim_facility
from transform import clean_source, transform_dim_facility
from load import load_dim_facility
from create_warehouse import create
from connect import connect_local_sql_server_2016, engine_local_sql_server_2016

import pandas as pd

# connect to the target database and run startup DDL script
connection = connect_local_sql_server_2016()
engine = engine_local_sql_server_2016()
create(connection)


# read source data
df = read_source_file()

# perform initial type conversions and codify redacted data
df = clean_source(df)

# extract, transform, and load dim_Facility
print('Processing Dim_Facility..')
dim_facility = extract_dim_facility(df)
dim_facility = transform_dim_facility(dim_facility, 0)
load_dim_facility(dim_facility, engine)






