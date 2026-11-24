import os
import sys
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
for name, file in [("players", "players_clean"), ("matches", "matches_clean"),
                   ("sessions", "sessions_clean"), ("patches", "patches")]:
    df = pd.read_csv(f"data/{file}.csv")
    for col in df.columns:
        if col.endswith("_date"):
            df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
    df.to_sql(name, con, index=False)

sql_file = sys.argv[1]
result = pd.read_sql_query(open(sql_file).read(), con)
print(result.to_string(index=False))

# Also save the result as a CSV in the output folder (for the dashboard)
os.makedirs("output", exist_ok=True)
out_file = os.path.join("output", os.path.basename(sql_file).replace(".sql", ".csv"))
result.to_csv(out_file, index=False)
print(f"\nSaved to {out_file}")