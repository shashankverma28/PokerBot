RANKS = "23456789TJQKA"


def rank_index(card):
    return RANKS.index(card.rank)


def has_flush_draw(cards, board):

    if len(board) < 3:
        return False

    suits = {}

    for c in cards + board:
        suits[c.suit] = suits.get(c.suit, 0) + 1

    return any(count == 4 for count in suits.values())


def has_straight_draw(cards, board):

    if len(board) < 3:
        return False

    ranks = set(rank_index(c) for c in cards + board)

    for start in range(10):
        window = set(range(start, start + 4))
        if len(window & ranks) >= 4:
            return True

    return False


def has_overcards(cards, board):

    if not board:
        return False

    board_high = max(rank_index(c) for c in board)
    card_ranks = [rank_index(c) for c in cards]

    return any(r > board_high for r in card_ranks)


def detect_draw(cards, board):

    flush = has_flush_draw(cards, board)
    straight = has_straight_draw(cards, board)
    over = has_overcards(cards, board)

    return {
        "flush_draw": flush,
        "straight_draw": straight,
        "overcards": over,
        "any_draw": flush or straight or over
    }
