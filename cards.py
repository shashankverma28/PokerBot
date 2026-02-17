RANKS = "23456789TJQKA"
SUITS = "cdhs"   # clubs, diamonds, hearts, spades


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"


def parse_card(card_str):
    """
    Example:
    'Ah' -> Ace of hearts
    'Td' -> Ten of diamonds
    """
    rank = card_str[0]
    suit = card_str[1]
    return Card(rank, suit)


def parse_cards(card_list):
    return [parse_card(c) for c in card_list]
