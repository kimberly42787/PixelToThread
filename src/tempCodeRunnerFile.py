distances, indices = nbrs.kneighbors(rgb_df[["Centroids_Red", "Centroids_Green", "Centroids_Blue"]])
        # matched_dmc = dmc_df.iloc[indices.flatten()].reset_index(drop=True)
        # matched_dmc['Distance'] = distances.flatten()  # optional: show distance
        # result = pd.concat([rgb_df.reset_index(drop=True), matched_dmc], axis=1)
        # output_file = f"output: {filename}.csv"
        # filepath = os.path.join(output_folder, output_file)
        # result.to_csv(filepath, index=False)