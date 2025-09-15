import pandas as pd

url = "https://dmc.crazyartzone.com/dmc_to_hex.php?color="

tables = pd.read_html(url)

dmc_df = tables[0]

dmc_df.to_csv("dmc_rgb.csv", index=False)

clean_dmc_df = dmc_df[~dmc_df["Floss Name"].str.contains("adsbygoogle", na=False)]
clean_dmc_df.to_csv("clean_dmc_rgb.csv", index=False)
print(clean_dmc_df)