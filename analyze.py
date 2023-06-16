import pandas as pd
import pathlib

tournaments = pd.read_json("data/full/fwango_tournaments_230613.json")
tournaments.to_csv("data/full/fwango_tournaments_230613.csv", index=False)

players = pd.DataFrame()
for file in pathlib.Path("data/").glob("fwango_players*"):
    month = file.stem.split("_")[2]
    year = file.stem.split("_")[3]
    df = pd.read_json(file, typ="series").to_frame("count")
    df["month"] = month
    df["year"] = year
    players = pd.concat([players, df])
players.reset_index(names="name").to_csv("data/full/fwango_players_230613.csv", index=False)
players.groupby(["month", "year"]).sum().reset_index().to_csv("data/full/fwango_players_agg_230613.csv", index=False)