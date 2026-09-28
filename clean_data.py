import pandas as pd

players = pd.read_csv("data/players.csv", parse_dates=["signup_date"])
matches = pd.read_csv("data/matches.csv", parse_dates=["match_date"])
sessions = pd.read_csv("data/sessions.csv", parse_dates=["session_date"])

print("BEFORE cleaning")
print("missing region:", players["region"].isnull().sum())
print("missing headshot_pct:", matches["headshot_pct"].isnull().sum())
print("map values:", sorted(matches["map"].unique()))
print("duplicate sessions:", sessions.duplicated().sum())

# 1. Missing regions -> label as Unknown
players["region"] = players["region"].fillna("Unknown")

# 2. Messy map names -> remove spaces, fix capitalization
matches["map"] = matches["map"].str.strip().str.title()

# 3. Missing headshot % -> fill with the median (only ~1% of rows)
matches["headshot_pct"] = matches["headshot_pct"].fillna(matches["headshot_pct"].median())

# 4. Duplicate sessions -> drop
sessions = sessions.drop_duplicates()

print("\nAFTER cleaning")
print("missing region:", players["region"].isnull().sum())
print("missing headshot_pct:", matches["headshot_pct"].isnull().sum())
print("map values:", sorted(matches["map"].unique()))
print("duplicate sessions:", sessions.duplicated().sum())

players.to_csv("data/players_clean.csv", index=False)
matches.to_csv("data/matches_clean.csv", index=False)
sessions.to_csv("data/sessions_clean.csv", index=False)
print("\nSaved *_clean.csv files")