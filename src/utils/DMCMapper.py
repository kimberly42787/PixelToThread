import pandas as pd
import numpy as np
from skimage import color
import math

class DMCMapper:
    
    def __init__(self, dmc_csv):

        self.dmc_df = pd.read_csv(dmc_csv)
        self.dmc_df = self.dmc_df.dropna(subset=["Red", "Green", "Blue"])

        # Convert the values into a numpy array
        self.dmc_rgb = self.dmc_df[["Red", "Green", "Blue"]].values.astype(np.uint8)

        # Transfer values into LAB values for computation later
        self.dmc_lab = color.rgb2lab(self.dmc_rgb[np.newaxis, :, :] / 255.0)[0]


    # METRICS TO TEST
    ### euclidean
    ### weighted euclidean 
    ### deltaE2000

    def euclidean_rgb(self, c1, c2):
        # Regular Euclidean distance equation
        r1, g1, b1 = c1
        r2, g2, b2 = c2
        return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
    
    def weighted_euclidean(self, c1, c2):
        # Weighted euclidean (using 2, 4, 3)
        (r1, g1, b1) = c1
        (r2, g2, b2) = c2
        return math.sqrt(2 * ((r1-r2)**2) + 4*((g1-g2)**2) + 3*((b1-b2)**2))
    
    def lab_E2000(self, c1, c2=None):
        c1_lab = color.rgb2lab(c1[np.newaxis, np.newaxis, :] / 255.0)[0, 0, :]
        return color.deltaE_ciede2000(c1_lab[np.newaxis, :], self.dmc_lab)
    
    # MAPPING FUNCTIONS
    def map_color(self, rgb_pixel, method="lab"):
        # Map RGB pixels to the closest DMC thread

        rgb_pixel = np.array(rgb_pixel, dtype=np.uint8)

        if method == "euclidean":
            dists = np.sum((self.dmc_rgb - rgb_pixel) ** 2, axis = 1)

        elif method == "weighted":
            diffs = self.dmc_rgb - rgb_pixel
            dists = np.sqrt(2 * diffs[:, 0] ** 2 + 4 * diffs[:, 1] ** 2 + 3 * diffs[:, 2] ** 2)

        elif method == "lab":
            dists = self.lab_E2000(rgb_pixel)

        else: 
            raise ValueError("Unknown method!")
        
        idx = np.argmin(dists)

        return {
            "DMC": self.dmc_df.iloc[idx]["DMC"],
            "Name": self.dmc_df.iloc[idx]["Floss Name"],
            "RGB": (
                int(self.dmc_df.iloc[idx]["Red"]),
                int(self.dmc_df.iloc[idx]["Green"]),
                int(self.dmc_df.iloc[idx]["Blue"])
            )
        }
    
    def map_image(self, img, method="lab"):
        # Map an image to the nearest DMC threads
        # Returns an image with the DMC RGB colors

        h, w, _ = img.shape
        mapped_img = np.zeros_like(img)

        for i in range(h):
            for j in range(w):
                mapped = self.map_color(img[i,j], method = method)
                mapped_img[i,j] = mapped["RGB"]

        return mapped_img