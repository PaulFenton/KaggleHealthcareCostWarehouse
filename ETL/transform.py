import pandas as pd
import numpy as np

def clean_source(df):

    # deal with nulls in Operating Certificate Number
    #df['Facility Id'] = df['Facility Id'].fillna(0).astype('int64')
    df['Operating Certificate Number'] = df['Operating Certificate Number'].fillna(4000).astype('int64') # use certificate # 4000 to indicate identifying information was redacted for abortion procedure

    # deal with nulls in Facility Id
    df['Facility Id'] = df['Facility Id'].fillna(4000).astype('int64') # use facility code 4000 to indicate identifying information was redacted for abortion procedure

    # deal with '120 +' in length of stay
    df['Length of Stay'] = df['Length of Stay'].replace('120 +', 120).astype('float64')

    # get rid of the $ sign in costs and parse as float
    df['Total Charges'] = df['Total Charges'].replace('[\$,]', '', regex=True).astype(float)
    df['Total Costs'] = df['Total Costs'].replace('[\$,]', '', regex=True).astype(float)

    # calculate profit in transformation to simplify reporting
    df['Total Profit'] = df['Total Charges'] - df['Total Costs']

    return df

def transform_dim_facility(df, startdate):

    # extract the facility dimension from the main DF
    dim = df.groupby(['Facility Id']).agg({
        'Health Service Area': 'first',
        'Hospital County': 'first',
        'Operating Certificate Number': 'first',
        'Facility Name': 'first'
    }).reset_index()

    # add the new SCD tracking columns
    dim['Active Flag'] = 1
    dim['Effective Start Date'] = startdate
    dim['Effective End Date'] = np.nan

    return dim

def transform_dim_diagnosis(df, startdate):

    # extract the facility dimension from the main DF
    dim = df.groupby(['CCS Diagnosis Code']).agg({
        'CCS Diagnosis Description': 'first'
    }).reset_index()

    # add the new SCD tracking columns
    #dim['Active Flag'] = 1
    #dim['Effective Start Date'] = startdate
    #dim['Effective End Date'] = np.nan

    return dim

def transform_dim_procedure(df, startdate):

    # extract the facility dimension from the main DF
    dim = df.groupby(['CCS Procedure Code']).agg({
        'CCS Procedure Description': 'first'
    }).reset_index()

    # add the new SCD tracking columns
    #dim['Active Flag'] = 1
    #dim['Effective Start Date'] = startdate
    #dim['Effective End Date'] = np.nan

    return dim

def transform_dim_provider(df, startdate):

    licenses = np.append(df['Attending Provider License Number'].unique(),
              df['Operating Provider License Number'].unique())

    licenses = np.append(licenses, df['Other Provider License Number'].unique())

    dim = pd.DataFrame(pd.Series(licenses).unique(), columns=['Provider License Number'])

    # add the new SCD tracking columns
    #dim['Active Flag'] = 1
    #dim['Effective Start Date'] = startdate
    #dim['Effective End Date'] = np.nan

    return dim