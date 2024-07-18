import pandas as pd
import os

# Grab all .xls files in the data folder
path = "../data"
extension = ".xls"
files = [file for file in os.listdir(path) if file.endswith(extension)]

# Combine all excel files into one dataframe
dfs = []
for file in files:
    df = pd.read_excel(os.path.join(path, file))
    dfs.append(df)


df = pd.concat(dfs, ignore_index=True)

df.to_csv("../data/housing_data.csv", index=False)
