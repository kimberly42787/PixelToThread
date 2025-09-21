
import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Data Subfolders
DMC_THREADS = os.path.join(DATA_DIR, "DMC Threads")
RGB_PALETTE = os.path.join(DATA_DIR, "RGB Palette")
RGB_DMC_MAPPING = os.path.join(DATA_DIR, "RGB DMC Mapping")
KMEANS_IMAGES = os.path.join(DATA_DIR, "KMEANS Images")
UNMAPPED_COLORS = os.path.join(DATA_DIR, "UNMAPPED COLORS")

# Make sure folder exist
os.makedirs(DMC_THREADS, exist_ok=True)
os.makedirs(RGB_PALETTE, exist_ok=True)
os.makedirs(RGB_DMC_MAPPING, exist_ok=True)
os.makedirs(KMEANS_IMAGES, exist_ok=True)
os.makedirs(UNMAPPED_COLORS, exist_ok=True)

# File Paths
CLEAN_DMC_CSV = os.path.join(DMC_THREADS, "clean_dmc_threads.csv")


