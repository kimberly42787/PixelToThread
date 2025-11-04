from PIL import Image
import numpy as np

class PILQuantizer:
    """
    Uses PIL's quantize() to reduce colors.
    """
    def quantize_image(self, img_array, n_colors):
        """
        pil_img: PIL.Image.Image (RGB)
        """

        # If input is numpy array, convert it to PIL.Image
        if isinstance(img_array, np.ndarray):
            # ensure RGB mode
            pil_img = Image.fromarray(img_array.astype("uint8"), "RGB")
        else:
            pil_img = img_array

        # Quantize to n_colors using Median Cut
        quantized = pil_img.quantize(colors=n_colors, method=Image.MEDIANCUT)

        return quantized
