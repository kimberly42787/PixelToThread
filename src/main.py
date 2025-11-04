import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from src.utils.DMCMapper import DMCMapper
from src.utils.DMC_colors import save_dmc_colors
from src.utils.ProcessImage import ProcessImage
from src.utils.PILQuantize import PILQuantizer
from src.utils.KMEANS import applyKmeans
from src.utils.PatternGrid import PatternGrid
from src.utils.DMCList import DMCList
from src.utils.DMC_reducer import DMCColorReducer
from config import CLEAN_DMC_CSV

import logging

# Configure Logging
logging.basicConfig(
    level = logging.DEBUG,
    format = "[%(levelname)s] %(asctime)s - %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def main():
    
    #---------------------------------------------------------------------------------------------------------------#
    # Read image and pixelate
    #---------------------------------------------------------------------------------------------------------------#

    image_path = "/Users/kim/Desktop/repos/PixelToThread/images/simple.png"
    csi = ProcessImage(image_path)

    # Example: 5x7 inch image, 14 stitches per inch
    grid_img, resized_img, w_stitches, h_stitches = csi.pixelate(20.0, 16.0, 16.0)

    print(f"Pixelated to {w_stitches} x {h_stitches} stitches")

    # Convert to numpy for mapping
    grid_np = np.array(grid_img)

    #-------------------------------------------------------------------------------------------------------------------#
    # Map to the DMC thread colors
    #-------------------------------------------------------------------------------------------------------------------#

    dmc = DMCMapper(CLEAN_DMC_CSV)

    # Try different methods
    mapped_euclidean = dmc.map_image(grid_np, method="euclidean")
    mapped_weighted = dmc.map_image(grid_np, method="weighted")
    mapped_lab = dmc.map_image(grid_np, method="lab")
    mapped_pil = Image.fromarray(mapped_lab.astype("uint8"))

    #-------------------------------------------------------------------------------------------------------------------#
    # Assign number of colors 
    #-------------------------------------------------------------------------------------------------------------------#
       
    n_colors = 100

    #-------------------------------------------------------------------------------------------------------------------#
    # Apply Kmeans
    #-------------------------------------------------------------------------------------------------------------------#
    
    km_q = applyKmeans()

    km_img= km_q.quantize_Kmeans(mapped_lab, n_colors=n_colors)

    #-------------------------------------------------------------------------------------------------------------------#
    # Reduce Colors on DMC Mapped Image
    #-------------------------------------------------------------------------------------------------------------------#

    dmc_list = pd.read_csv(CLEAN_DMC_CSV)

    reducer = DMCColorReducer(n_colors=n_colors, dmc_list=dmc_list)

    reduced_img = reducer.reduce_image(mapped_lab)

    pil_img = Image.fromarray(reduced_img)

    df_colors = reducer.get_color_counts(reduced_img)

    list_dmc = DMCList()

    merged_csv = list_dmc.get_thread_list(df_colors, CLEAN_DMC_CSV)

    logger.info(merged_csv.head())

    #-------------------------------------------------------------------------------------------------------------------#
    # Apply Grid Overlay on the Kmeans Quantized Image
    #-------------------------------------------------------------------------------------------------------------------#
    
    pg = PatternGrid(cell_size=1, line_thickness=1, major_every=10, upscale=20)

    grid_img = pg.apply_grid(reduced_img)

    #-------------------------------------------------------------------------------------------------------------------#
    # Visualize - Original Pixelated, Mapped DMC Image, Kmeans, Grid Overlay
    #-------------------------------------------------------------------------------------------------------------------#


    fig, axes = plt.subplots(1, 5, figsize=(18, 6))

    # Images
    axes[0].imshow(grid_np)
    axes[0].set_title("Original Pixelated")
    axes[0].axis("off")

    axes[1].imshow(mapped_lab)
    axes[1].set_title("DMC Mapped Image")
    axes[1].axis("off")
 
    axes[2].imshow(km_img)
    axes[2].set_title(f"KMeans: ({n_colors} colors)")
    axes[2].axis("off")

    axes[3].imshow(pil_img)
    axes[3].set_title("Reduced Threads")
    axes[3].axis("off")

    axes[4].imshow(grid_img)
    axes[4].set_title("Grid Overlay")
    axes[4].axis("off")

    plt.tight_layout()
    plt.savefig("Picture_Progression_With_Arrows.png", dpi=300)
    plt.show()
        
if __name__ == "__main__":
    main()