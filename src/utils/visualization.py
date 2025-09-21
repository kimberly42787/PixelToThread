import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from config import RGB_DMC_MAPPING, UNMAPPED_COLORS

def visualize_unmapped(height, width):
    """
    Show an image where unmapped pixels are highlighted in green.
    """

    input_folder = RGB_DMC_MAPPING
    output_folder = UNMAPPED_COLORS


    for filename in os.listdir(input_folder):
        with open(os.path.join(input_folder, filename)) as f:
            mapped_df = pd.read_csv(f)
            mapped_colors = mapped_df[['Red.1','Green.1','Blue.1']].values.reshape(height, width, 3)

            mask = mapped_df['Unmapped'].values.reshape(height, width)
            mapped_colors[mask] = [0,255,0]

            plt.imshow(mapped_colors.astype(np.uint8))
            plt.title("Mapped DMC with unmapped pixels highlighted in green")
            plt.axis('off')

            output_paht = os.path.join(output_folder, )
            plt.show()