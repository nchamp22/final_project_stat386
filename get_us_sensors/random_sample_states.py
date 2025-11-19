import pandas as pd

df = pd.read_csv("US_Locations.csv")

sampled_df = (
    df.groupby("State", group_keys=False)
      .apply(lambda x: x.sample(n=25) if len(x) > 20 else x)
)


sampled_df.to_csv("US_Locations_Sampled.csv", index=False)

print(len(sampled_df))