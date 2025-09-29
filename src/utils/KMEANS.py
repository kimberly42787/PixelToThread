from sklearn.cluster import KMeans
import numpy as np


class applyKmeans:

    def quantize_Kmeans(self, img, n_colors):
        
        h, w, _ = img.shape
        pixels = img.reshape(-1,3)

        # Run Kmeans 
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        labels = kmeans.fit_predict(pixels)
        centers = np.round(kmeans.cluster_centers_).astype(np.uint8)

        kmeans_img = centers[labels].reshape(h, w, 3)

        return kmeans_img