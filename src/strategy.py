import copy


class Node:
    """
    :param monster: the card_id of the monster
    """
    def __init__(self, card):
        self._card = card
        self._heat = 1
        self._children = {}

    @property
    def card(self):
        return self._card

    @property
    def mana(self):
        return self._card.mana

    @property
    def heat(self):
        return self._heat

    def add_children(self, monsters):
        first_monster = monsters[0]
        if first_monster.id in self._children:
            if len(monsters[1:]) > 0:
                self._children[first_monster.id].add_children(monsters[1:])
        else:
            child = Node(first_monster)
            self._children[first_monster.id] = child
            if len(monsters[1:]) > 0:
                child.add_children(monsters[1:])
        self._heat += 1

    def get_next_best(self, chosen, mana_cap):
        max_heat = -1
        best_card = None
        children_id = None
        for c_id, c in self._children.items():
            if c.heat > max_heat and mana_cap >= c.mana:
                max_heat = c.heat
                best_card = c.card
                children_id = c_id
        if best_card is None:
            return chosen
        else:
            chosen.append(copy.deepcopy(best_card))
            return self._children[children_id].get_next_best(chosen, mana_cap - best_card.mana)


class Strategy:
    """
    Recurrent algorithm.
    input : color + mana cap
    output at each step : monster to choose
    """
    def __init__(self, deck, games):
        self._deck = deck
        self._games = games

    def get_team(self, mana_cap, color):
        sub_deck = [c for c in self._deck.cards if c.color == color]
        color_filtered_games = [g for g in self._games if g["winner"]["color"] == color]
        filtered_games = []
        for game in color_filtered_games:
            mana_used = sum([self._deck.get_card_by_id(m["card_id"]).mana for m in game["winner"]["monsters"]])
            if mana_used in [mana_cap, mana_cap - 1]:
                filtered_games.append(game)
        tree = self.as_tree(sub_deck, filtered_games)
        return tree.get_next_best([], mana_cap)

    def as_tree(self, deck, games):
        root = Node(None)
        for game in games:
            winning_team = game["winner"]
            root.add_children([self._deck.get_card_by_id(c["card_id"]) for c in winning_team["monsters"]])
        return root

    def get_best_color(self, mana_cap):
        win_rate = {}
        for game in self._games:
            mana_used = sum([self._deck.get_card_by_id(m["card_id"]).mana for m in game["winner"]["monsters"]])
            if mana_used in [mana_cap, mana_cap - 1]:
                color_pick = game["winner"]["color"]
                if color_pick in win_rate:
                    win_rate[color_pick] += 1
                else:
                    win_rate[color_pick] = 1
        best_win_rate = max(win_rate.values())
        color = {v: k for k, v in win_rate.items()}[best_win_rate]
        return color
