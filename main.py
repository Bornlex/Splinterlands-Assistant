import sys
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


def read_cards():
    starter_df = pd.read_csv("starter.csv", index_col="name", delimiter="\t")
    with open("data/cards.json") as f:
        raw_data = json.load(f)
    monsters, summoners = [], []
    for d in raw_data:
        if d["type"] == "Monster":
            monsters.append(
                card.Monster(
                    d["id"],
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
            summoners.append(card.Summoner(
                d["name"],
                d["color"],
                d["stats"]["abilities"] if "abilities" in d["stats"] else [],
                d["is_starter"]
            ))
    return monsters, summoners


def format_games(games, deck):
    df = pd.DataFrame(columns=["color", "1", "2", "3", "4", "5", "6", "sum(mana)"])
    for game in games:
        winning_team = game["winner"]
        row = {"color": winning_team["color"]}
        mana = 0
        for i, monster in enumerate(winning_team["monsters"]):
            row[f"{i + 1}"] = deck.get_card_by_id(monster["card_id"]).name
            mana += deck.get_card_by_id(monster["card_id"]).mana
        row["sum(mana)"] = mana
        df = df.append(row, ignore_index=True)
    return df


if __name__ == '__main__':
    cards, summoners = read_cards()
    deck = card.Deck(cards)
    with open("games.json") as f:
        games_df = format_games(json.load(f)["games"], deck)
    games_df.to_csv("games.csv", index=False)
    engine = strategy.Strategy(cards)
    while True:
        try:
            color_input = input("Color : ")
            mana_cap = int(input("Mana cap : "))
            selection = engine.get_deck(mana_cap, color_input)
            for c in selection:
                print(f"Name: {c.name}, Cost: {c.mana}")
        except (EOFError, KeyboardInterrupt):
            sys.exit(1)
