import pandas as pd
from sklearn.neighbors import NearestNeighbors
import os
from config import CLEAN_DMC_CSV, RGB_PALETTE, RGB_DMC_MAPPING

def map_rgb_to_dmc():

    input_folder = RGB_PALETTE
    output_folder = RGB_DMC_MAPPING
    
    # Read DMC thread csv
    dmc_df = pd.read_csv(CLEAN_DMC_CSV)
    print(dmc_df)

    nbrs = NearestNeighbors(n_neighbors=1, metric="euclidean")
    nbrs.fit(dmc_df[["Red", "Green", "Blue"]])

    for filename in os.listdir(input_folder):
        with open(os.path.join(input_folder, filename)) as f:
            rgb_df = pd.read_csv(f)
            distances, indices = nbrs.kneighbors(rgb_df[["Red", "Green", "Blue"]])
            matched_dmc = dmc_df.iloc[indices.flatten()].reset_index(drop=True)
            matched_dmc['Distance'] = distances.flatten()  # optional: show distance
            print(matched_dmc)
            result = pd.concat([rgb_df.reset_index(drop=True), matched_dmc], axis=1)
            output_file = f"output: {filename}"
            filepath = os.path.join(output_folder, output_file)
            result.to_csv(filepath, index=False)

