import json
import pandas as pd

from src import card, api, strategy


def save_scoring(values):
    df = pd.DataFrame(values, columns=card.Monster.dataframe_columns())
    df = df.sort_values("score", ascending=False)
    df.to_csv("basic_scoring.csv")


def save_games(values, columns):
    df = pd.DataFrame(values, columns=columns)
    df.to_csv("games.csv")


if __name__ == '__main__':
    starter_df = pd.read_csv("starter.csv", index_col="name", delimiter="\t")
    with open("data/cards.json") as f:
        raw_data = json.load(f)
    cards = []
    for d in raw_data:
        if d["type"] == "Monster":
            cards.append(
                card.Monster(
                    d["name"],
                    d["color"],
                    d["stats"]["mana"],
                    d["stats"]["attack"],
                    d["stats"]["ranged"],
                    d["stats"]["armor"],
                    d["stats"]["health"],
                    d["stats"]["speed"],
                    d["stats"]["abilities"],
                    starter_df.loc[d["name"]]["is_starter"]
                )
            )
        elif d["type"] == "Summoner":
            card.Summoner(
                d["name"],
                d["color"],
                d["stats"]["abilities"] if "abilities" in d["stats"] else [],
                d["is_starter"]
            )

    print(len(results))
