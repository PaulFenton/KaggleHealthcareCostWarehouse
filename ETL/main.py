from extract import read_source_file
from transform import clean_source, transform_dim_facility, transform_dim_diagnosis, transform_dim_procedure, transform_dim_provider
from load import load_dim
from create_warehouse import create
from connect import connect_local_sql_server_2016, engine_local_sql_server_2016
import pandas as pd

# util functions
def merge(df, dim, dim_columns, join_label):
    # merge with the dimension table to get the Key and remove the string key
    count = df.count()[0]
    df = pd.merge(df, dim[dim_columns], on=join_label, how='left').drop([join_label], axis=1)
    print("Merged with " + str(count- df.count()[0]) +  " records dropped.")
    return df

def process_dimension(df, table_name, transformer, loader, join_label, index_label, engine):
    print('Transforming ' + table_name + '..')
    dim = transformer(df, 0)
    print('Loading ' + table_name + '..')
    load_dim(dim, table_name, engine)
    dim[index_label] = dim.index + 1  # database will assign this key scheme automatically, recreate it to help pandas map the fact table keys

    print('Encoding fact table keys for ' + table_name + '..')
    df = merge(df, dim, [index_label, join_label], join_label)
    return df, dim

# connect to the target database and run startup DDL script
connection = connect_local_sql_server_2016()
engine = engine_local_sql_server_2016()
create(connection)


# read source data
df = read_source_file()

# perform initial type conversions and codify redacted data
df = clean_source(df)

# transform and load dim_Facility
df, dim_Facility = process_dimension(df, 'dim_Facility', transform_dim_facility, load_dim, 'Facility Id', 'Facility Key', engine)

# transform and load dim_Classifications_Diag
df, dim_Classifcations_Diag = process_dimension(df, 'dim_Classifications_Diag', transform_dim_diagnosis, load_dim, 'CCS Diagnosis Code', 'Classifications_Diag_Key', engine)

# transform and load dim_Classifications_Proc
df, dim_Classifications_Proc = process_dimension(df, 'dim_Classifications_Proc', transform_dim_procedure, load_dim, 'CCS Procedure Code', 'Classifications_Proc_Key', engine)

# transform and load dim_Provider
#df, dim_Provider = process_dimension(df, 'dim_Provider', transform_dim_provider, load_dim, 'Provider License Number', 'Provider_Key', engine)