from methods import pixelate_img, apply_kmeans
import cv2
import pandas as pd
import os

# TEST IMAGE
img_path = "/Users/kim/Desktop/repos/PixelToThread/images/newyork.png"


grid_img, resized_img, w_stitches, h_stitches = pixelate_img(img_path, width_in=5.50, height_in=8.0, spi=14)

print(f"Stitch Resolution: {w_stitches} x {h_stitches}")

cv2.imshow("Turned to BGR", cv2.cvtColor(resized_img, cv2.COLOR_RGB2BGR))

# List of K options
color_options = [150, 100, 75, 20, 4]

# Store results
clustered_previews = []

os.makedirs("RGB Palettes", exist_ok=True)

for k in color_options:
    clustered_small, palette = apply_kmeans(grid_img, k)

    # Save preview image
    clustered_preview = cv2.resize(
        clustered_small, resized_img.shape[1::-1], interpolation=cv2.INTER_AREA
    )
    clustered_previews.append(clustered_preview)

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
    print(palette_df.head())
    filename = f"palette_k{k}.csv"
    filepath = os.path.join("RGB Palettes", filename)
    palette_df.to_csv(filepath, index=False)
    print(f"Saved {filepath}")


# Display results side by side
for i, k in enumerate(color_options):
    cv2.imshow(f"K={k}", cv2.cvtColor(clustered_previews[i], cv2.COLOR_RGB2BGR))

cv2.waitKey(0)
cv2.destroyAllWindows()




