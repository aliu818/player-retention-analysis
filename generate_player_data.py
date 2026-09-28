"""
Generates a SIMULATED competitive-shooter player dataset for the
"Player Retention & Churn Analysis" portfolio project.

Run:  python generate_player_data.py
Needs: pip install pandas numpy

Outputs 4 CSVs in ./data/ :  players, matches, sessions, patches
The data has churn patterns deliberately built in (rank-wall churn,
a bad patch, channel quality differences). Your job in the project is
to FIND them with SQL/Python and explain them. Say in your README
that the data is simulated and how it was generated.
"""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
os.makedirs("data", exist_ok=True)

N_PLAYERS = 5000
START, END = pd.Timestamp("2025-01-01"), pd.Timestamp("2025-06-30")
DAYS = (END - START).days

RANKS = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond"]
MAPS = ["Ascent", "Bind", "Haven", "Split", "Lotus"]
AGENTS = ["Duelist_A", "Duelist_B", "Controller", "Sentinel", "Initiator"]
CHANNELS = ["Organic", "Friend Referral", "Paid Ads", "Streamer"]
REGIONS = ["NA-West", "NA-East", "EU", "APAC"]
PLATFORMS = ["PC", "Console"]

# Patches (patch 3 is a "bad" balance patch that hurts retention)
patches = pd.DataFrame({
    "patch_id": ["1.0", "2.0", "3.0", "4.0"],
    "release_date": pd.to_datetime(["2025-01-01", "2025-02-15", "2025-04-01", "2025-05-15"]),
    "note": ["Launch", "New map (Lotus)", "Weapon rebalance", "Ranked reset"],
})

# ---- Players ----
signup = START + pd.to_timedelta(rng.integers(0, DAYS - 14, N_PLAYERS), unit="D")
players = pd.DataFrame({
    "player_id": np.arange(1, N_PLAYERS + 1),
    "signup_date": signup,
    "region": rng.choice(REGIONS, N_PLAYERS, p=[.3, .2, .3, .2]),
    "platform": rng.choice(PLATFORMS, N_PLAYERS, p=[.7, .3]),
    "acquisition_channel": rng.choice(CHANNELS, N_PLAYERS, p=[.35, .25, .25, .15]),
})
# Channel quality: paid ads churn faster, referrals stick
channel_factor = players["acquisition_channel"].map(
    {"Organic": 1.0, "Friend Referral": 1.5, "Paid Ads": 0.6, "Streamer": 0.9}).values

# Total active lifetime in days (heavy-tailed)
lifetime = rng.exponential(30 * channel_factor)
players["life_days"] = lifetime

match_rows, session_rows = [], []
match_id = session_id = 1
for p in players.itertuples():
    rank_idx = 1  # everyone starts at Bronze
    skill = rng.normal(0, 1)
    day = 0
    active_days = int(min(p.life_days, (END - p.signup_date).days))
    while day <= active_days:
        date = p.signup_date + pd.Timedelta(days=day)
        # Rank wall: stuck at Gold -> extra chance to quit
        if RANKS[rank_idx] == "Gold" and rng.random() < 0.06:
            break
        # Patch 3 (bad rebalance): players who were active then may quit
        if date >= patches.release_date[2] and date < patches.release_date[2] + pd.Timedelta(days=7) \
                and rng.random() < 0.10:
            break
        n_matches = max(1, int(rng.poisson(3)))
        dur = float(np.clip(rng.normal(25 * n_matches, 15), 10, 300))
        session_rows.append((session_id, p.player_id, date, round(dur, 1)))
        session_id += 1
        for _ in range(n_matches):
            hs = float(np.clip(rng.normal(22 + 3 * skill, 6), 2, 55))
            win_p = float(np.clip(0.5 + 0.03 * skill + 0.004 * (hs - 22), 0.2, 0.8))
            win = int(rng.random() < win_p)
            kills = int(np.clip(rng.normal(14 + 3 * skill, 5), 0, 40))
            deaths = int(np.clip(rng.normal(14 - 1.5 * skill, 4), 1, 35))
            match_rows.append((match_id, p.player_id, date, rng.choice(MAPS),
                               rng.choice(AGENTS), RANKS[rank_idx], win,
                               kills, deaths, round(hs, 1)))
            match_id += 1
            if win and rng.random() < 0.08 and rank_idx < len(RANKS) - 1:
                rank_idx += 1
            elif not win and rng.random() < 0.05 and rank_idx > 0:
                rank_idx -= 1
        day += int(rng.geometric(0.45))  # gap until next play day

matches = pd.DataFrame(match_rows, columns=[
    "match_id", "player_id", "match_date", "map", "agent", "rank_tier",
    "win", "kills", "deaths", "headshot_pct"])
sessions = pd.DataFrame(session_rows, columns=[
    "session_id", "player_id", "session_date", "duration_min"])

# ---- Make it "messy" on purpose so you can practice cleaning ----
matches.loc[matches.sample(frac=0.01, random_state=1).index, "headshot_pct"] = np.nan
matches.loc[matches.sample(frac=0.005, random_state=2).index, "map"] = "  bind "
players.loc[players.sample(frac=0.02, random_state=3).index, "region"] = None
sessions = pd.concat([sessions, sessions.sample(50, random_state=4)])  # duplicates

players = players.drop(columns="life_days")
players.to_csv("data/players.csv", index=False)
matches.to_csv("data/matches.csv", index=False)
sessions.to_csv("data/sessions.csv", index=False)
patches.to_csv("data/patches.csv", index=False)
print(f"players={len(players):,} matches={len(matches):,} sessions={len(sessions):,}")
