from extract import read_source_file, read_dim_date
from transform import clean_source,\
    transform_dim_facility,\
    transform_dim_diagnosis,\
    transform_dim_procedure,\
    transform_dim_provider,\
    transform_dim_patients_refine,\
    transform_dim_patients
from load import load_dim
from create_warehouse import create
from connect import connect_local_sql_server_2016, engine_local_sql_server_2016
import pandas as pd
import numpy as np

source_path = "../source_data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv"
date_path = "../source_data/date.csv"

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
    if(isinstance(join_label, list)):
        join_label.append(index_label)
        columns = join_label
    else:
        columns = [index_label, join_label]
    df = merge(df, dim, columns, join_label)
    return df, dim

# connect to the target database and run startup DDL script
connection = connect_local_sql_server_2016()
engine = engine_local_sql_server_2016()
create(connection)


# read source data
df = read_source_file(source_path)

# perform initial type conversions and codify redacted data
df = clean_source(df)

# transform and load dim_Facility
df, dim_Facility = process_dimension(df, 'dim_Facility', transform_dim_facility, load_dim, 'Facility Id', 'Facility_Key', engine)
df = df.drop(['Health Service Area', 'Hospital County', 'Operating Certificate Number', 'Facility Name'], axis=1)

# transform and load dim_Classifications_Diag
df, dim_Classifcations_Diag = process_dimension(df, 'dim_Classifications_Diag', transform_dim_diagnosis, load_dim, 'CCS Diagnosis Code', 'Classifications_Diag_Key', engine)
df = df.drop(['CCS Diagnosis Description'], axis=1)

# transform and load dim_Classifications_Proc
df, dim_Classifications_Proc = process_dimension(df, 'dim_Classifications_Proc', transform_dim_procedure, load_dim, 'CCS Procedure Code', 'Classifications_Proc_Key', engine)
df = df.drop(['CCS Procedure Description'], axis=1)

# transform and load the patients refine table
df, dim_Patients_Refine = process_dimension(df, 'dim_Patients_Refine', transform_dim_patients_refine, load_dim, 'APR DRG Code', 'Patients_Refine_Key', engine)
df = df.drop(['APR Risk of Mortality'], axis=1)

# transform and load the patients junk table
#df, dim_Patients = process_dimension(df, 'dim_Patient', transform_dim_patients, load_dim, ['Age Group', 'Zip Code - 3 digits', 'Gender', 'Race', 'Ethnicity', 'Patient Disposition'], 'Patient_Key', engine)

# transform and load dim_Provider
#df, dim_Provider = process_dimension(df, 'dim_Provider', transform_dim_provider, load_dim, 'Provider License Number', 'Provider_Key', engine)
dim_Provider = transform_dim_provider(df, 0)
load_dim(dim_Provider, 'dim_Provider', engine)
dim_Provider['Provider_Key'] = dim_Provider.index + 1
dim_Provider['Provider License Number'] = dim_Provider['Provider License Number'].astype(str) #change type to object to allow joining with nullable column
count = df.count()[0]
df = pd.merge(df, dim_Provider[['Provider_Key', 'Provider License Number']], left_on='Attending Provider License Number', right_on='Provider License Number', how='left').drop(['Provider License Number'], axis=1)
df = df.rename(columns={'Provider_Key': 'Attending_Provider_Key'})
df = pd.merge(df, dim_Provider[['Provider_Key', 'Provider License Number']], left_on='Operating Provider License Number', right_on='Provider License Number', how='left').drop(['Provider License Number'], axis=1)
df = df.rename(columns={'Provider_Key': 'Operating_Provider_Key'})
df = pd.merge(df, dim_Provider[['Provider_Key', 'Provider License Number']], left_on='Other Provider License Number', right_on='Provider License Number', how='left').drop(['Provider License Number'], axis=1)
df = df.rename(columns={'Provider_Key': 'Other_Provider_Key'})
df = df.drop(['Attending Provider License Number', 'Operating Provider License Number', 'Other Provider License Number'], axis=1)
print("Merged with " + str(count- df.count()[0]) + " records dropped.")

# extract from file and load the constructed dim_Date table
dim_Date = read_dim_date(date_path)
load_dim(dim_Date, 'dim_Date', engine)
dim_Date['Date_Key'] = dim_Date.index + 1
# put a random date column on the fact table to simulate usage of the date dimension
df['Date_Key'] = np.random.randint(dim_Date['Date_Key'].min(), dim_Date['Date_Key'].max(), df.shape[0])


count = df.count()[0]
df = df.groupby(['Date_Key', 'Facility_Key', 'Classifications_Diag_Key', 'Classifications_Proc_Key', 'Patients_Refine_Key']).agg({
    'Attending_Provider_Key': 'first',
    'Operating_Provider_Key': 'first',
    'Other_Provider_Key': 'first',
    'Length of Stay': 'mean',
    'Birth Weight': 'mean',
    'Total Costs': sum,
    'Total Charges': sum,
    'Total Profit': sum
}).reset_index()

load_dim(df, 'fact_Procedure_Cost', engine)

