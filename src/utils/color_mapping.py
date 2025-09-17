import pandas as pd
import os

# Make a dictionary for the centroid RGB to the DMC RGB
input_folder = "/Users/kim/Desktop/repos/PixelToThread/Mapping Output"
output_folder = "Color Dictionary"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    map_df = pd.read_csv(os.path.join(input_folder,filename))
    map_df = map_df.rename(columns={
        "Red":"K_Red",
        "Green": "K_Green",
        "Blue": "K_Blue",
        "Red.1":"DMC_Red",
        "Green.1":"DMC_Green",
        "Blue.1": "DMC_Blue"
    })

    mapping = {}
    for _, row in map.df.iterrows():
        mapping[tuple(row[["K_Red", "K_Green", "K_Blue"]])] = tuple(row[["DMC_Red", "DMC_Green", "DMC_Blue"]])


    
