from extract import read_source_file, clean_source


import pandas as pd

# read source data
df = read_source_file()

# perform initial type conversions and codify redacted data
df = clean_source(df)

