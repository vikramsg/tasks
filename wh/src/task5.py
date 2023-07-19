from typing import List
import pandas as pd


def sample():
    original_df = pd.read_csv("data/origin_data.csv")

    # Calculate distribution
    fruit_probs = original_df["favourite_fruit"].value_counts(normalize=True)

    to_sample_df = pd.read_csv("data/data_to_sample.csv")
    to_sample_df["weights"] = to_sample_df["favourite_fruit"].map(fruit_probs)

    sampled_df = to_sample_df.sample(n=5000, weights="weights")


if __name__ == "__main__":
    sample()
