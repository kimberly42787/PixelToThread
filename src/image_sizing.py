import cv2
from image_reader import read_image

res_presets = {
    "low" : (300,300),
    "medium" : (600,600),
    "high" : (1000,1000)
}

def pixelate_with_cv2(image_path, preset="medium"):

    # Load RGB image
    img = read_image(image_path)

    # Assign target size to the preset selected
    target_size = res_presets[preset]

    # Downscale to the target size
    grid_img = cv2.resize(img, target_size, interpolation=cv2.INTER_NEAREST)

    # Resize back to original size
    preview_img = cv2.resize(grid_img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

    #Return both
    return grid_img, preview_img

