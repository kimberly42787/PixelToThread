import cv2
import numpy as np
import matplotlib.pyplot as plt

class PatternGrid:

    def __init__(self, cell_size=1, line_thickness=1, major_every=10, upscale=1):
        self.cell_size = cell_size
        self.line_thickness = line_thickness
        self.major_every = major_every
        self.upscale = upscale

    def apply_grid(self, img):

        if self.upscale > 1:
            img = cv2.resize(
                img,
                (img.shape[1] * self.upscale, img.shape[0] * self.upscale),
                interpolation=cv2.INTER_NEAREST
            )
            cell_size = self.cell_size * self.upscale
        else:
            cell_size = self.cell_size

        grid_img = img.copy()
        h, w, _ = grid_img.shape

        # Draw vertical lines
        for x in range(0, w, cell_size):
            if (x // cell_size) % self.major_every == 0:
                color = (0, 0, 0)   # black for major lines
                thickness = self.line_thickness + 1
            else:
                color = (50, 50, 50)  
                thickness = self.line_thickness
            cv2.line(grid_img, (x, 0), (x, h), color, thickness)

        # Draw horizontal lines
        for y in range(0, h, cell_size):
            if (y // cell_size) % self.major_every == 0:
                color = (0, 0, 0)
                thickness = self.line_thickness + 1
            else:
                color = (50, 50, 50)
                thickness = self.line_thickness
            cv2.line(grid_img, (0, y), (w, y), color, thickness)

        return grid_img

    def show(self, img, title="Cross-Stitch Pattern with Grid"):
        """
        Display the grid overlayed image with matplotlib.
        """
        grid_img = self.apply_grid(img)
        plt.figure(figsize=(10, 10))
        plt.imshow(grid_img)
        plt.axis("off")
        plt.title(title)
        plt.show()