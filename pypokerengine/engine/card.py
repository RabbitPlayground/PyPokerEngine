class Card:

    DIAMOND = 2
    CLUB = 4
    HEART = 8
    SPADE = 16

    SUIT_MAP = {
        2: 'd',
        4: 'c',
        8: 'h',
        16: 's'
    }

    RANK_MAP = {
        1: '2',
        2: '3',
        3: '4',
        4: '5',
        5: '6',
        6: '7',
        7: '8',
        8: '9',
        9: 'T',
        10: 'J',
        11: 'Q',
        12: 'K',
        13: 'A'
    }

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        print(str(self), str(other))
        return self.suit == other.suit and self.rank == other.rank

    def __str__(self):
        return f'{self.RANK_MAP[self.rank]}{self.SUIT_MAP[self.suit].lower()}'

    def to_id(self):
        num = 0
        tmp = self.suit >> 1
        while tmp & 1 != 1:
            num += 1
            tmp >>= 1

        return self.rank + 13 * num

    @classmethod
    def from_id(cls, card_id):
        suit, rank = 2, card_id
        while rank > 13:
            suit <<= 1
            rank -= 13

        return cls(suit, rank)

    @classmethod
    def from_str(cls, str_card):
        assert(len(str_card) == 2)

        def inverse(hsh):
            return {v: k for k, v in hsh.items()}

        rank = inverse(cls.RANK_MAP)[str_card[0]]
        suit = inverse(cls.SUIT_MAP)[str_card[1].lower()]
        return cls(suit, rank)
