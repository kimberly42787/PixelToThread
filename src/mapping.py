import pandas as pd

# Read DMC thread csv
dmc_df = pd.read_csv("dmc_rgb.csv")
print(dmc_df.dtypes)
print(len(dmc_df))

dmc_df = dmc_df[~dmc_df["Floss Name"].str.contains("adsbygoogle", na=False)]






print(dmc_df.info())
print(dmc_df.head())