from PIL import Image
import numpy as np

class PILQuantizer:
    """
    Uses PIL's quantize() to reduce colors.
    """
    def quantize_image(self, pil_img, n_colors):
        """
        pil_img: PIL.Image.Image (RGB)
        """
        # Quantize with median-cut
        quantized = pil_img.quantize(colors=n_colors, method=Image.MEDIANCUT)
        quantized = quantized.convert("RGB")  # Back to RGB
        np_img = np.array(quantized)
        
        return np_img