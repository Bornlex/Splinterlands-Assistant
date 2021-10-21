import json
import requests


class API:
    base_route_history = "https://api.splinterlands.io/battle/history?player="
    base_route_leaderboard = "https://api.splinterlands.io/players/leaderboard"

    @staticmethod
    def extract_team_info(team):
        return {
            "player": team["player"],
            "rating": team["rating"],
            "color": team["color"],
            "summoner": {
                "card_id": team["summoner"]["card_detail_id"],
                "level": team["summoner"]["level"]
            },
            "monsters": [{
                "card_id": m["card_detail_id"],
                "level": m["level"],
            } for m in team["monsters"]]
        }

    @staticmethod
    def get_player_games(player):
        route = f"{API.base_route_history}{player}"
        response = requests.get(route)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_leaderboard():
        response = requests.get(API.base_route_leaderboard)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_latest_games_from_leaderboard():
        results = []
        best_players = API.get_leaderboard()
        for player in best_players:
            games = API.get_player_games(player["player"])
            for game in games["battles"]:
                details = json.loads(game["details"])
                if "type" in details and details["type"]:
                    continue
                team1 = API.extract_team_info(details["team1"])
                team2 = API.extract_team_info(details["team2"])
                winner = details["winner"]
                loser = details["loser"]
                results.append({
                    "winner": team1 if team1["player"] == winner else team2,
                    "loser": team1 if team1["player"] == loser else team2
                })
        return results
