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

    # add some calculated columns to simplify reporting # todo should we do this?
    df['Total Profit'] = df['Total Charges'] - df['Total Costs']
    df['Profit Margin'] = df['Total Profit'].divide(df['Total Charges'])

    return df

def transform_dim_facility(df, startdate):

    # add the new SCD tracking columns
    df['Active Flag'] = 1
    df['Effective Start Date'] = startdate
    df['Effective End Date'] = np.nan

    return df