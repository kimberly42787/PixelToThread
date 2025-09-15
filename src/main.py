from methods import pixelate_img, apply_kmeans, map_to_dmc
import cv2
import pandas as pd
import os

# TEST IMAGE
img_path = "/Users/kim/Desktop/repos/PixelToThread/images/newyork.png"

grid_img, resized_img, w_stitches, h_stitches = pixelate_img(img_path, width_in=5.50, height_in=8.0, spi=14)

print(f"Stitch Resolution: {w_stitches} x {h_stitches}")

cv2.imshow("Turned to BGR", cv2.cvtColor(resized_img, cv2.COLOR_RGB2BGR))




# List of K options
color_options = [200, 125, 75, 20, 5]

# Store results
clustered_previews = []

os.makedirs("RGB Palettes", exist_ok=True)
os.makedirs("Mapped Images", exist_ok=True)




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
    filepath = os.path.join("RGB Palettes", filename)
    palette_df.to_csv(filepath, index=False)
    print(f"Saved {filepath}")

mapped_previews = []
for k, clustered_preview in clustered_previews:
    palette_csv_path = os.path.join("Mapping Output", f"output: palette_k{k}.csv")  # your mapped CSV
    if os.path.exists(palette_csv_path):
        dmc_palette_df = pd.read_csv(palette_csv_path)

        # Optional: drop NaNs to avoid conversion errors
        dmc_palette_df = dmc_palette_df.dropna(subset=["Red.1", "Green.1", "Blue.1"])

        mapped_img = map_to_dmc(clustered_preview, dmc_palette_df)
        mapped_previews.append((k, mapped_img))

        # Save mapped image
        mapped_path = os.path.join("Mapped Images", f"newyork_k{k}_dmc.png")
        cv2.imwrite(mapped_path, cv2.cvtColor(mapped_img, cv2.COLOR_RGB2BGR))
        print(f"Mapped image saved: {mapped_path}")
    else:
        print(f"⚠️ Mapped CSV not found for K={k}, skipping mapping.")

# --- Step 4: Display previews ---
for k, preview in clustered_previews:
    cv2.imshow(f"KMeans K={k}", cv2.cvtColor(preview, cv2.COLOR_RGB2BGR))

for k, mapped_img in mapped_previews:
    cv2.imshow(f"DMC Mapped K={k}", cv2.cvtColor(mapped_img, cv2.COLOR_RGB2BGR))

cv2.waitKey(0)
cv2.destroyAllWindows()