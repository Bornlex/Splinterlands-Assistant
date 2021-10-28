class Monster:
    def __init__(self, card_id, name, color, mana, attack, ranged, armor, health, speed, abilities, is_starter):
        self._id = card_id
        self._name = name
        self._color = color
        self._mana = mana
        self._attack = attack
        self._ranged = ranged
        self._armor = armor
        self._health = health
        self._speed = speed
        self._abilities = abilities
        self._is_starter = is_starter
        self._level = 0
        self._max_level = len(self._mana) - 1

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def mana(self):
        return self._mana[self._level]

    @property
    def attack(self):
        return self._attack[self._level]

    @property
    def ranged(self):
        return self._ranged[self._level]

    @property
    def armor(self):
        return self._armor[self._level]

    @property
    def health(self):
        return self._health[self._level]

    @property
    def speed(self):
        return self._speed[self._level]

    @property
    def abilities(self):
        res = []
        for i in range(self.level + 1):
            res += self._abilities[i]
        return res

    @property
    def is_starter(self):
        return self._is_starter

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        assert self._max_level <= new_level < 0
        self._level = new_level

    def as_dataframe_row(self):
        """
        Does not return abilities yet.
        """
        return [
            self.name, self.color, self.is_starter, self.mana, self.attack,
            self.ranged, self.armor, self.health, self.speed,
            len(self.abilities), self.score()
        ]

    def score(self):
        """
        Returns the score per mana unit.
        """
        if self.mana == 0:
            return self.attack + self.ranged + self.armor + self.health + self.speed + len(self.abilities)
        return (self.attack + self.ranged + self.armor + self.health + self.speed + len(self.abilities)) / self.mana

    @staticmethod
    def dataframe_columns():
        return [
            "name", "color", "is starter", "mana", "attack", "ranged", "armor",
            "health", "speed", "len(abilities)", "score"
        ]


class Summoner:
    def __init__(self, name, color, abilities, is_starter):
        self._name = name
        self._color = color
        self._abilities = abilities
        self._is_starter = is_starter

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def abilities(self):
        return self._abilities

    @property
    def is_starter(self):
        return self._is_starter


class Deck:
    def __init__(self, cards, summoners):
        self._cards = cards
        self._summoners = summoners

    @property
    def cards(self):
        return self._cards

    def get_card_by_id(self, card_id):
        for c in self._cards:
            if c.id == card_id:
                return c

    def get_summoner_by_color(self, color):
        for s in self._summoners:
            if s.color == color:
                return s
