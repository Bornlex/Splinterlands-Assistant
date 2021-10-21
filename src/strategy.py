class Strategy:
    def __init__(self, cards):
        self._cards = cards

    def get_deck(self, mana_cap, color):
        sub_deck = [c for c in self._cards if c.color == color]
