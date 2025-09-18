


import cv2
import pandas as pd
import os

from src.utils.DMC_colors import save_dmc_colors
from src.utils.methods import pixelate_img, apply_kmeans, map_to_dmc
from src.utils.mapping import map_rgb_to_dmc
from config import RGB_PALETTE, KMEANS_IMAGES, RGB_DMC_MAPPING

import logging

# Configure Logging
logging.basicConfig(
    level = logging.DEBUG,
    format = "[%(levelname)s] %(asctime)s - %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():

    logger.info("Starting cross stitch pipeline")

    try:
        # Fetch and save DMC thread csv file 
        clean_dmc_df = save_dmc_colors()
        logger.info("Fetch DMC threads csv successfully")
        logger.debug("Preview:\n%s", clean_dmc_df)

        # Test image
        img_path = "/Users/kim/Desktop/repos/PixelToThread/images/newyork.png"
        
        # Read image
        grid_img, resized_img, w_stitches, h_stitches = pixelate_img(img_path, width_in=5.0, height_in=7.0, spi=14)
        logger.info(f"Stitch Resolution: {w_stitches} x {h_stitches}")
        cv2.imshow("Turned to BGR", cv2.cvtColor(resized_img, cv2.COLOR_RGB2BGR))

        # Use KMEANS to make cluster of RGB
        color_options = [300, 400, 200, 100, 50, 5]
        clustered_previews = []

        map_rgb_to_dmc()
        logger.info("Mapped RGB to DMC is successful!")
        
        for k in color_options:
            clustered_small, palette = apply_kmeans(grid_img, k)

            # Save preview image
            clustered_preview = cv2.resize(
                clustered_small, resized_img.shape[1::-1], interpolation=cv2.INTER_AREA
            )
            clustered_previews.append((k, clustered_preview))

            # Save palette (one row per color)
            palette_records = []

            for i, rgb in enumerate(palette):
                palette_records.append({
                    "K": k,
                    "ColorID": i,
                    "Red": int(rgb[0]),
                    "Green": int(rgb[1]),
                    "Blue": int(rgb[2])
                })

            # Convert to DataFrame and save
            palette_df = pd.DataFrame(palette_records)
            filename = f"palette_k{k}.csv"
            filepath = os.path.join(RGB_PALETTE, filename)
            palette_df.to_csv(filepath, index=False)
            print(f"Saved {filepath}")



            # Mapping to the DMC colors
            mapped_previews = []

            for k, clustered_preview in clustered_previews:
                mapping_csv_path = os.path.join(RGB_DMC_MAPPING, f"output: palette_k{k}.csv")

                if os.path.exists(mapping_csv_path):
                    dmc_palette_df = pd.read_csv(mapping_csv_path)

                    # Optional: drop NaNs to avoid conversion errors
                    dmc_palette_df = dmc_palette_df.dropna(subset=["Red.1", "Green.1", "Blue.1"])

                    mapped_img = map_to_dmc(clustered_preview, dmc_palette_df)
                    mapped_previews.append((k, mapped_img))

                    # Save mapped image
                    mapped_path = os.path.join(KMEANS_IMAGES, f"philippines:{k}_dmc.png")
                    cv2.imwrite(mapped_path, cv2.cvtColor(mapped_img, cv2.COLOR_RGB2BGR))
                    print(f"Mapped image saved: {mapped_path}")
                else:
                    print(f"Mapped CSV not found for K={k}, skipping mapping.")

        # --- Step 4: Display previews ---
        for k, preview in clustered_previews:
            cv2.imshow(f"KMeans K={k}", cv2.cvtColor(preview, cv2.COLOR_RGB2BGR))

        for k, mapped_img in mapped_previews:
            cv2.imshow(f"DMC Mapped K={k}", cv2.cvtColor(mapped_img, cv2.COLOR_RGB2BGR))

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        logger.error("Error occured", e, exc_info=True)

if __name__ == "__main__":
    main()


# # List of K options
# color_options = [200, 125, 75, 20, 5]

# # Store results
# clustered_previews = []

# os.makedirs("RGB Palettes", exist_ok=True)
# os.makedirs("Mapped Images", exist_ok=True)




# for k in color_options:
#     clustered_small, palette = apply_kmeans(grid_img, k)

#     # Save preview image
#     clustered_preview = cv2.resize(
#         clustered_small, resized_img.shape[1::-1], interpolation=cv2.INTER_AREA
#     )
#     clustered_previews.append((k, clustered_preview))

#     # Save palette (one row per color)
#     palette_records = []
#     for i, rgb in enumerate(palette):
#         palette_records.append({
#             "K": k,
#             "ColorID": i,
#             "Red": int(rgb[0]),
#             "Green": int(rgb[1]),
#             "Blue": int(rgb[2])
#         })

#     # Convert to DataFrame and save
#     palette_df = pd.DataFrame(palette_records)
#     filename = f"palette_k{k}.csv"
#     filepath = os.path.join("RGB Palettes", filename)
#     palette_df.to_csv(filepath, index=False)
#     print(f"Saved {filepath}")

# mapped_previews = []
# for k, clustered_preview in clustered_previews:
#     palette_csv_path = os.path.join("Mapping Output", f"output: palette_k{k}.csv")  # your mapped CSV
#     if os.path.exists(palette_csv_path):
#         dmc_palette_df = pd.read_csv(palette_csv_path)

#         # Optional: drop NaNs to avoid conversion errors
#         dmc_palette_df = dmc_palette_df.dropna(subset=["Red.1", "Green.1", "Blue.1"])

#         mapped_img = map_to_dmc(clustered_preview, dmc_palette_df)
#         mapped_previews.append((k, mapped_img))

#         # Save mapped image
#         mapped_path = os.path.join("Mapped Images", f"newyork_k{k}_dmc.png")
#         cv2.imwrite(mapped_path, cv2.cvtColor(mapped_img, cv2.COLOR_RGB2BGR))
#         print(f"Mapped image saved: {mapped_path}")
#     else:
#         print(f"⚠️ Mapped CSV not found for K={k}, skipping mapping.")

# # --- Step 4: Display previews ---
# for k, preview in clustered_previews:
#     cv2.imshow(f"KMeans K={k}", cv2.cvtColor(preview, cv2.COLOR_RGB2BGR))

# for k, mapped_img in mapped_previews:
#     cv2.imshow(f"DMC Mapped K={k}", cv2.cvtColor(mapped_img, cv2.COLOR_RGB2BGR))

# cv2.waitKey(0)
# cv2.destroyAllWindows()