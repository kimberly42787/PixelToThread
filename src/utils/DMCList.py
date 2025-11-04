
import pandas as pd
import numpy as np
from PIL import Image

class DMCList:

    def get_thread_list(self, mapped_df, dmc_path):

        mapped_df = mapped_df

        dmc_df = pd.read_csv(dmc_path)

        merged_df = pd.merge(
            dmc_df, 
            mapped_df,
            how= "inner",
            on=["Hex Code"]
        )
        
        merged_df.to_csv("merged.csv", index=False)
        return merged_df
    
