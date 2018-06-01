import pandas as pd
def extract():
    df = pd.read_csv("../source_data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv", low_memory=False, error_bad_lines=False)

    # todo: do something here

    return df