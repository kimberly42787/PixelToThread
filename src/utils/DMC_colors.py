
"""
Scrape the DMC thread colors and their corresponding RGB fronm dmc.crazyartzone
Saves cleaned CSV file
"""

import pandas as pd
from config import CLEAN_DMC_CSV

def save_dmc_colors():
    # URL to scrape the dmc threads
    url = "https://dmc.crazyartzone.com/dmc_to_hex.php?color="

    # Read DMC thread table and save as a dataframe
    tables = pd.read_html(url)
    dmc_df = tables[0]

    # Clean the table
    clean_dmc_df = dmc_df[~dmc_df["Floss Name"].str.contains("adsbygoogle", na=False)]

    # Save as a CSV file
    clean_dmc_df.to_csv(CLEAN_DMC_CSV, index=False)

    return clean_dmc_df
