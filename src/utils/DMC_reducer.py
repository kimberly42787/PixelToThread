
import numpy as np
import pandas as pd
from PIL import Image

class DMCColorReducer:
    """
    Reduce the number of colors in a DMC-mapped image while
    keeping only valid DMC thread colors.
    """

    def __init__(self, n_colors=20, dmc_list=None):
        """
        n_colors: number of DMC colors to keep in the reduced image
        dmc_list: full DMC list as Nx3 array or DataFrame with columns ['Red','Green','Blue']
        """
        self.n_colors = n_colors
        if isinstance(dmc_list, pd.DataFrame):
            self.dmc_list = dmc_list[['Red','Green','Blue']].values
        elif isinstance(dmc_list, np.ndarray):
            self.dmc_list = dmc_list
        else:
            raise ValueError("dmc_list must be a DataFrame or numpy array")
        self.top_colors = None

    def reduce_image(self, img_array):
        """
        img_array: numpy array (HxWx3), already mapped to DMC RGB
        Returns:
            reduced_img: HxWx3 numpy array with exactly n_colors
            top_colors: list of RGB colors used
        """
        pixels = img_array.reshape(-1, 3)

        # Count occurrences of each color in the image
        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)

        # Sort by frequency
        sorted_idx = np.argsort(-counts)
        top_colors = unique_colors[sorted_idx]

        # If fewer than n_colors, fill with nearest DMC colors not in top_colors
        if len(top_colors) < self.n_colors:
            remaining = self.n_colors - len(top_colors)
            # Compute distances from DMC list to top_colors
            candidates = []
            for dmc_color in self.dmc_list:
                if not any(np.array_equal(dmc_color, c) for c in top_colors):
                    # compute distance to top_colors
                    dist = np.min(np.sum((top_colors - dmc_color) ** 2, axis=1))
                    candidates.append((dist, dmc_color))
            candidates.sort(key=lambda x: x[0])
            # Add closest remaining colors
            extra_colors = [c[1] for c in candidates[:remaining]]
            top_colors = np.vstack([top_colors, extra_colors])

        else:
            # take top n_colors
            top_colors = top_colors[:self.n_colors]

        self.top_colors = top_colors

        # Map each pixel to nearest top color
        def nearest_top_color(color):
            distances = np.sum((self.top_colors - color) ** 2, axis=1)
            return self.top_colors[np.argmin(distances)]

        reduced_pixels = np.array([nearest_top_color(pixel) for pixel in pixels], dtype=np.uint8)
        reduced_img = reduced_pixels.reshape(img_array.shape)

        return reduced_img
    
    def get_color_counts(self, img):

        pixels = img.reshape(-1, 3)

        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)

        df_colors = pd.DataFrame(
            [(int(r), int(g), int(b), int(cnt)) for (r, g, b), cnt in zip(unique_colors, counts)],
            columns=["Red", "Green", "Blue", "Count"]
        )

        df_colors["Hex Code"] = df_colors.apply(
            lambda row: "#{:02X}{:02X}{:02X}".format(row["Red"], row["Green"], row["Blue"]),
            axis=1
        )

        df_colors.to_csv("DMC Thread Colors", index=False)

        return df_colors




   # def __init__(self, n_colors=20):
    #     """
    #     n_colors: number of DMC colors to keep in the reduced image
    #     """
    #     self.n_colors = n_colors
    #     self.top_colors = None

    # def reduce_image(self, img_array):
    #     """
    #     img_array: numpy array (HxWx3), already mapped to DMC RGB
    #     Returns:
    #         reduced_img: HxWx3 numpy array with only n_colors
    #         top_colors: list of RGB colors used
    #     """
    #     # Flatten image
    #     pixels = img_array.reshape(-1, 3)

    #     # Count occurrences of each DMC color
    #     unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)

    #     # Sort by frequency
    #     sorted_idx = np.argsort(-counts)
    #     self.top_colors = unique_colors[sorted_idx][:self.n_colors]

    #     # Map all pixels to nearest top color
    #     def nearest_top_color(color):
    #         distances = np.sum((self.top_colors - color) ** 2, axis=1)
    #         return self.top_colors[np.argmin(distances)]

    #     reduced_pixels = np.array([nearest_top_color(pixel) for pixel in pixels], dtype=np.uint8)
    #     reduced_img = reduced_pixels.reshape(img_array.shape)

    #     return reduced_img