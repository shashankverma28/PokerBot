# board_texture.py

RANKS = "23456789TJQKA"


def rank_index(card):
    return RANKS.index(card.rank)


def suit_counts(board):
    suits = {}
    for c in board:
        suits[c.suit] = suits.get(c.suit, 0) + 1
    return suits


def is_paired(board):
    ranks = [c.rank for c in board]
    return len(set(ranks)) < len(ranks)


def is_monotone(board):
    return max(suit_counts(board).values()) == len(board)


def is_two_tone(board):
    return max(suit_counts(board).values()) == 2


def connectivity_score(board):
    ranks = sorted(rank_index(c) for c in board)
    gaps = [ranks[i+1] - ranks[i] for i in range(len(ranks)-1)]
    return sum(gaps)


def has_ace(board):
    return any(c.rank == "A" for c in board)


def high_cards(board):
    return sum(rank_index(c) >= 9 for c in board)  # T or higher


# ----------------------------------
# Main classifier
# ----------------------------------

def classify_board(board):

    if len(board) < 3:
        return {"texture": "none", "wet": False}

    paired = is_paired(board)
    mono = is_monotone(board)
    two_tone = is_two_tone(board)

    conn = connectivity_score(board)
    ace_present = has_ace(board)
    high = high_cards(board)

    # -------- Category Logic --------

    if paired:
        texture = "paired"

    elif mono:
        texture = "monotone"

    elif conn <= 3 and two_tone:
        texture = "wet_heavy"

    elif conn <= 3:
        texture = "connected"

    elif two_tone:
        texture = "two_tone"

    elif ace_present and high >= 2:
        texture = "ace_dynamic"

    elif high >= 1:
        texture = "dry_high"

    else:
        texture = "dry_low"

    # Wetness approximation
    wet = texture in {"connected", "wet_heavy", "monotone", "two_tone"}

    return {
        "texture": texture,
        "wet": wet,
        "paired": paired,
        "monotone": mono,
        "two_tone": two_tone,
        "connected_score": conn,
        "ace_present": ace_present
    }
