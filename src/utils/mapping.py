import pandas as pd
from sklearn.neighbors import NearestNeighbors
import os
from config import CLEAN_DMC_CSV, RGB_PALETTE, RGB_DMC_MAPPING

def map_rgb_to_dmc(distance_threshold=20):

    input_folder = RGB_PALETTE
    output_folder = RGB_DMC_MAPPING
    
    # Read DMC thread csv
    dmc_df = pd.read_csv(CLEAN_DMC_CSV)
    dmc_df[["Red","Green","Blue"]] = dmc_df[["Red","Green","Blue"]].clip(0,255).astype(int)
    print(dmc_df)

    nbrs = NearestNeighbors(n_neighbors=1, metric="euclidean")
    nbrs.fit(dmc_df[["Red", "Green", "Blue"]].values)

    for filename in os.listdir(input_folder):
        with open(os.path.join(input_folder, filename)) as f:
            rgb_df = pd.read_csv(f)
            rgb_df[["Red","Green","Blue"]] = rgb_df[["Red","Green","Blue"]].clip(0,255).astype(int)

            # Map to nearest DMC
            distances, indices = nbrs.kneighbors(rgb_df[["Red", "Green", "Blue"]].values)
            matched_dmc = dmc_df.iloc[indices.flatten()].reset_index(drop=True)
            matched_dmc['Distance'] = distances.flatten()  
            print(matched_dmc)

            # Flag pixels that are far
            rgb_df['Unmapped'] = distances.flatten() > distance_threshold
            result = pd.concat([rgb_df.reset_index(drop=True), matched_dmc], axis=1)

            output_file = f"mapped_{filename}"
            filepath = os.path.join(output_folder, output_file)
            result.to_csv(filepath, index=False)
            print(f"Saved {output_file} | Unmapped pixels: {result['Unmapped'].sum()}")


