import cv2
import matplotlib.pyplot as plt

def read_image(image_path):

    img_bgr = cv2.imread(image_path)

    if img_bgr is None:
        raise FileNotFoundError("Cannot read file.")
    
    # Convert image from BGR to RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    return img_rgb

def bgr_vs_rgb(path):

    img_bgr = read_image(path, as_rgb=False)
    img_rgb = read_image(path, as_rgb=True)

    plt.figure (figsize=(8,5))

    # BGR display
    plt.subplot(1,2,1)
    plt.imshow(img_bgr)
    plt.title("BGR - OpenCV default")
    plt.axis("off")

    # RGB display
    plt.subplot(1,2,2)
    plt.imshow(img_rgb)
    plt.title("RGB - Matplotlib")
    plt.axis("off")

    plt.show()

