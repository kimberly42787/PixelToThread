import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


def read_image(image_path):

    img_bgr = cv2.imread(image_path)

    if img_bgr is None:
        raise FileNotFoundError("Cannot read file.")
    
    # Convert image from BGR to RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    return img_rgb


def pixelate_img(img_path, width_in, height_in, spi):
 
    # Calculate the stitch resolution
    stitch_width = int(round(width_in * spi))
    stitch_height = int(round(height_in * spi))

    img = read_image(img_path)

    # Downscale image based on the stitch resolution
    grid_img = cv2.resize(img, (stitch_width,stitch_height), interpolation=cv2.INTER_AREA)

    # Scale back the image
    resized_img = cv2.resize(grid_img, img.shape[1::-1], interpolation=cv2.INTER_AREA)

    return grid_img, resized_img, stitch_width, stitch_height

def apply_kmeans(img, num_colors):

    # Flatten the pixels
    pixels = img.reshape(-1,3)

    #Run the kmeans
    kmeans = KMeans(n_clusters=num_colors, random_state=42)

    labels = kmeans.fit_predict(pixels)

    palette = kmeans.cluster_centers_.astype(np.uint8)

    #Replace pixels with clusteres centers
    clustered = palette[labels].reshape(img.shape)

    return clustered, palette

def map_to_dmc(clustered_img, palette_df):
    palette_df = palette_df.rename(columns={
        "Red":"K_Red",
        "Green": "K_Green",
        "Blue": "K_Blue",
        "Red.1":"DMC_Red",
        "Green.1":"DMC_Green",
        "Blue.1": "DMC_Blue"
    })

    dmc_img = clustered_img.copy()

    for _, row in palette_df.iterrows():
        k_rgb = (row["K_Red"], row["K_Green"], row["K_Blue"])
        dmc_rgb = (row["DMC_Red"], row["DMC_Green"], row["DMC_Blue"])

        mask = (clustered_img == k_rgb).all(axis=2)
        dmc_img[mask] = dmc_rgb

    return dmc_img