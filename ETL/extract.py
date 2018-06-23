import pandas as pd
def extract():

    # 2.4 M rows in csv need to be read into a dataframe in chunks
    list = []
    for chunk in pd.read_csv("../source_data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv", chunksize=20000, low_memory=False, error_bad_lines=False):
        list.append(chunk)
    df = pd.concat(list, axis=0)
    del list

    return df