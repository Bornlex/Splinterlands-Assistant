class Strategy:
    """
    Recurrent algorithm.
    input : color + mana cap
    output at each step : monster to choose
    """
    def __init__(self, cards):
        self._cards = cards

    def get_deck(self, mana_cap, color):
        sub_deck = [c for c in self._cards if c.color == color]

    def backtest(self, games):
        pass
