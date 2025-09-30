import cv2
import matplotlib.pyplot as plt
import numpy as np

from src.utils.DMCMapper import DMCMapper
from src.utils.ProcessImage import ProcessImage
from src.utils.PILQuantize import PILQuantizer
from src.utils.KMEANS import applyKmeans
from src.utils.PatternGrid import PatternGrid
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

    image_path = "/Users/kim/Desktop/repos/PixelToThread/images/newyork.jpg"
    csi = ProcessImage(image_path)

    # Example: 5x7 inch image, 14 stitches per inch
    grid_img, resized_img, w_stitches, h_stitches = csi.pixelate(9.0, 12.0, 14.0)

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

    #-------------------------------------------------------------------------------------------------------------------#
    # Apply Kmeans
    #-------------------------------------------------------------------------------------------------------------------#
    km_q = applyKmeans()
    n_colors = 75

    pg = PatternGrid(cell_size=1, line_thickness=1, major_every=10, upscale=20)

    km_img= km_q.quantize_Kmeans(mapped_lab, n_colors=n_colors)

    #-------------------------------------------------------------------------------------------------------------------#
    # Apply Grid Overlay on the Kmeans Quantized Image
    #-------------------------------------------------------------------------------------------------------------------#

    grid_img = pg.apply_grid(km_img)

    #-------------------------------------------------------------------------------------------------------------------#
    # Visualize - Original Pixelated, Mapped DMC Image, Kmeans, Grid Overlay
    #-------------------------------------------------------------------------------------------------------------------#

    fig, axes = plt.subplots(1, 4, figsize=(14, 8))
    axes[0].imshow(grid_np)
    axes[0].set_title(f"Original Pixelated)")
    axes[0].axis("off")

    axes[1].imshow(mapped_lab)
    axes[1].set_title(f"DMC Mapped Image")
    axes[1].axis("off")

    axes[2].imshow(km_img)
    axes[2].set_title(f"KMeans: ({n_colors} colors)")
    axes[2].axis("off")

    axes[3].imshow(grid_img)
    axes[3].set_title(f"Grid Overlay")
    axes[3].axis("off")
    
    plt.savefig(f"Grid Overlay")
    plt.show()

if __name__ == "__main__":
    main()