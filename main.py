import os
import sys
import json
import pandas as pd
from multiprocessing import Pool

from src import card, api, strategy


def save_scoring(values):
    df = pd.DataFrame(values, columns=card.Monster.dataframe_columns())
    df = df.sort_values("score", ascending=False)
    df.to_csv("basic_scoring.csv")


def save_games(values, columns):
    df = pd.DataFrame(values, columns=columns)
    df.to_csv("games.csv")


def get_opponents_from_game(game, index):
    if index % 1000 == 0:
        print(f".{index}")
    new_games = []
    new_opponents = []
    try:
        player1 = game["player_1"]
        player2 = game["player_2"]
    except:
        return None, None
    try:
        results = api.API.get_player_games(player2)["battles"]
        new_opponents.append(player2)
        new_games.append(results)
    except:
        pass
    try:
        results = api.API.get_player_games(player1)["battles"]
        new_opponents.append(player1)
        new_games.append(results)
    except:
        pass
    return new_opponents, new_games


def get_opponents_from_player(player_name, generation=3):
    opponents = []
    games = []
    games_to_process = api.API.get_player_games(player_name)["battles"]
    while generation > 0:
        print(f"Generation: {generation}")
        new_games = []
        with Pool(os.cpu_count() - 2) as p:
            print(f"Processing {len(games_to_process)}...")
            sub_results = p.starmap(get_opponents_from_game, [(g, i) for i, g in enumerate(games_to_process)])
            for new_opponents, new_oppo_games in sub_results:
                if new_opponents is None:
                    continue
                try:
                    if new_opponents[0] not in opponents:
                        opponents.append(new_opponents[0])
                        games_to_add = [extract_game_info(game) for game in new_oppo_games[0]]
                        new_games += [game for game in games_to_add if game is not None]
                    if new_opponents[1] not in opponents:
                        opponents.append(new_opponents[1])
                        games_to_add = [extract_game_info(game) for game in new_oppo_games[1]]
                        new_games += [game for game in games_to_add if game is not None]
                except:
                    print(f"Found error at: {new_opponents}")
        games_to_process = new_games.copy()
        games += new_games.copy()
        generation -= 1
    return opponents, games


def extract_game_info(game):
    details = json.loads(game["details"])
    if "type" in details and details["type"]:
        return None
    team1 = api.API.extract_team_info(details["team1"])
    team2 = api.API.extract_team_info(details["team2"])
    winner = details["winner"]
    loser = details["loser"]
    return {
        "winner": team1 if team1["player"] == winner else team2,
        "loser": team1 if team1["player"] == loser else team2
    }


def get_game_for_player(player_name):
    results = []
    games = api.API.get_player_games(player_name)
    for game in games["battles"]:
        details = json.loads(game["details"])
        if "type" in details and details["type"]:
            continue
        team1 = api.API.extract_team_info(details["team1"])
        team2 = api.API.extract_team_info(details["team2"])
        winner = details["winner"]
        loser = details["loser"]
        results.append({
            "winner": team1 if team1["player"] == winner else team2,
            "loser": team1 if team1["player"] == loser else team2
        })
    return results


def get_games_from_players(player_names):
    with Pool(os.cpu_count() - 1) as p:
        sub_results = p.map(get_game_for_player, player_names)
    return [r for s in sub_results for r in s]


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
    reread = input("Refresh games from Splinterlands API ? ")
    if reread in ["true", "True"]:
        opponents, games = get_opponents_from_player("tantalid")
        with open("games.json", "w") as f:
            json.dump({"games": games}, f)
        print(f"Formatting...")
        games_df = format_games(games, deck)
        games_df.to_csv("games.csv", index=False)
    else:
        with open("games.json") as f:
            games = json.load(f)["games"]
    engine = strategy.Strategy(deck, games)
    while True:
        try:
            color_input = input("Color : ")
            mana_cap = int(input("Mana cap : "))
            selection = engine.get_team(mana_cap, color_input)
            for c in selection:
                print(f"Name: {c.name}, Cost: {c.mana}")
        except (EOFError, KeyboardInterrupt):
            sys.exit(1)
