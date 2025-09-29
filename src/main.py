import cv2
import matplotlib.pyplot as plt
import numpy as np

from src.utils.DMCMapper import DMCMapper
from src.utils.ProcessImage import ProcessImage
from src.utils.PILQuantize import PILQuantizer
from src.utils.KMEANS import applyKmeans
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
    
    #---------------------------#
    # Read image and pixelate
    #---------------------------#

    image_path = "/Users/kim/Desktop/repos/PixelToThread/images/7BEAEEEA-8824-4F4F-9DF5-626DCE65790C_1_105_c.jpeg"
    csi = ProcessImage(image_path)

    # Example: 5x7 inch image, 14 stitches per inch
    grid_img, resized_img, w_stitches, h_stitches = csi.pixelate(10.0, 16.0, 14.0)

    print(f"Pixelated to {w_stitches} x {h_stitches} stitches")

    # Convert to numpy for mapping
    grid_np = np.array(grid_img)

    #-------------------------------#
    # Map to the DMC thread colors
    #-------------------------------#

    dmc = DMCMapper(CLEAN_DMC_CSV)

    # Try different methods
    mapped_euclidean = dmc.map_image(grid_np, method="euclidean")
    mapped_weighted = dmc.map_image(grid_np, method="weighted")
    mapped_lab = dmc.map_image(grid_np, method="lab")

    #-------------------------------#
    # Visualize
    #-------------------------------#
    fig, ax = plt.subplots(figsize=(5, 7))
    ax.imshow(grid_np)
    ax.set_title("Original Pixelated")
    ax.axis("off")
    plt.show()

    # fig, ax = plt.subplots(figsize=(6,8))
    # ax.imshow(mapped_euclidean)
    # ax.set_title("Euclidean Pixelated")
    # ax.axis("off")
    # plt.show()

    # fig, ax = plt.subplots(figsize=(6,8))
    # ax.imshow(mapped_weighted)
    # ax.set_title("Weighted Pixelated")
    # ax.axis("off")
    # plt.show()

    fig, ax = plt.subplots(figsize=(5, 7))
    ax.imshow(mapped_lab)
    ax.set_title("DMC LAB ΔE2000")
    ax.axis("off")
    plt.show()

    #-------------------------------#
    # Apply Kmeans
    #-------------------------------#
    km_q = applyKmeans()
    n_colors_list = [5, 100]

    for n_colors in n_colors_list:
        km_img = km_q.quantize_Kmeans(mapped_lab, n_colors=n_colors)

        fig, ax = plt.subplots(figsize=(5, 7))
        ax.imshow(km_img)
        ax.set_title(f"KMeans Quantized ({n_colors} colors)")
        ax.axis("off")
        plt.show()

    #-------------------------------#
    # Apply Kmeans
    #-------------------------------#
    pil_q = PILQuantizer()
    
    for n_colors in n_colors_list:
        pil_img = pil_q.quantize_image(mapped_lab, n_colors=n_colors)

        fig, ax = plt.subplots(figsize=(5, 7))
        ax.imshow(km_img)
        ax.set_title(f"KMeans Quantized ({n_colors} colors)")
        ax.axis("off")
        plt.show()     


if __name__ == "__main__":
    main()