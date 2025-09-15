

import pandas as pd
import os

input_folder = "/Users/kim/Desktop/repos/PixelToThread/Mapping Output"


for filename in os.listdir(input_folder):

    df = pd.read_csv(os.path.join(input_folder,filename))

    nan_rows = df[df[["Red.1", "Green.1", "Blue.1"]].isna().any(axis=1)]

    if not nan_rows.empty:
        print(f"⚠️ {filename} has {len(nan_rows)} rows with NaN:")
        print(nan_rows)

        df_clean = df.dropna(subset=["Red.1", "Green.1", "Blue.1"])

        df_clean.to_csv(filename, index=False)
        print(f"✅ Dropped NaNs and updated {filename}")
    else:
        print(f"✅ {filename} has no NaNs")