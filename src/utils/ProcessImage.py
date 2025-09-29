import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image


class ProcessImage:

    def __init__(self, image_path):

        self.image_path = image_path
        self.img = self.read_image()
        self.reg_width, self.reg_height = self.img.size


    def read_image(self):

        # Make sure it's in RGB
        img = Image.open(self.image_path).convert("RGB")
        
        return img


    def pixelate(self, width_in, height_in, spi):
    
        # Calculate the stitch resolution
        stitch_width = int(round(width_in * spi))
        stitch_height = int(round(height_in * spi))

        grid_img = self.img.resize((stitch_width, stitch_height), resample=Image.NEAREST)

        resized_img = self.img.resize((self.reg_width, self.reg_height), resample=Image.NEAREST)

        return grid_img, resized_img, stitch_width, stitch_height

