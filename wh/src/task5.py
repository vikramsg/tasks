import pandas as pd
import numpy as np

# Read the dataset
df = pd.read_csv(
    "your_dataset.csv"
)  # Replace 'your_dataset.csv' with the path to your dataset

# Count the number of users liking each fruit
fruit_counts = df["favorite_fruit"].value_counts()

# Display the distribution of number of users liking each fruit
print(fruit_counts)

# Assuming you have another dataset with the same schema
another_df = pd.read_csv(
    "another_dataset.csv"
)  # Replace 'another_dataset.csv' with the path to your another dataset

# Sample from another dataset based on the distribution of the original dataset
sampled_df = another_df.sample(
    n=len(df), replace=True, weights=fruit_counts[df["favorite_fruit"]].values
)

# Display the sampled DataFrame
print(sampled_df)
