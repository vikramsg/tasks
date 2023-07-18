from typing import List
import pandas as pd
import numpy as np


def _distribution_original_data(file_name: str):
    df = pd.read_csv(file_name)

    return df["favorite_fruit"].value_counts()


def sample_from_data(file_name: str, distribution: List[int], n_samples: int):
    df = pd.read_csv(file_name)

    # Sample from another dataset based on the distribution of the original dataset
    sampled_df = df.sample(n=n_samples, replace=True, weights=distribution)

    # Display the sampled DataFrame
    print(sampled_df)


if __name__ == "__main__":
    distribution = _distribution_original_data("data/origin_data.csv")
    sample_from_data("data/data_to_sample.csv", distribution, 5000)
