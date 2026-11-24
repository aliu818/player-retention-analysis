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

sql = open(sys.argv[1]).read()
print(pd.read_sql_query(sql, con).to_string(index=False))