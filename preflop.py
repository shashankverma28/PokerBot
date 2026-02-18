import random

RANK_ORDER = "23456789TJQKA"


# -------------------------------------------------
# Card Utilities
# -------------------------------------------------

def card_rank(card):
    return card.rank


def card_suit(card):
    return card.suit


def rank_index(rank):
    return RANK_ORDER.index(rank)


def hand_key(c1, c2):

    r1 = card_rank(c1)
    r2 = card_rank(c2)

    s1 = card_suit(c1)
    s2 = card_suit(c2)

    # Order high → low
    if rank_index(r1) < rank_index(r2):
        r1, r2 = r2, r1
        s1, s2 = s2, s1

    suited = (s1 == s2)

    if r1 == r2:
        return r1 + r2

    return r1 + r2 + ("s" if suited else "o")


# -------------------------------------------------
# Hand Ranges
# -------------------------------------------------

STRONG_RANGE = {
    "AA", "KK", "QQ", "JJ", "TT",
    "AKs", "AQs", "AJs", "KQs",
    "AKo"
}

MEDIUM_RANGE = {
    "99", "88", "77",
    "ATs", "KJs", "QJs",
    "AQo", "KQo"
}

PLAYABLE_RANGE = {
    "66", "55", "44",
    "A9s", "A8s", "KTs", "QTs",
    "JTs", "T9s", "98s",
    "AJo", "KJo"
}

SPECULATIVE_RANGE = {
    "33", "22",
    "87s", "76s", "65s", "54s",
    "A5s", "A4s"
}


# -------------------------------------------------
# Decision Engine
# -------------------------------------------------

def preflop_decision(cards, state, opponent):

    c1, c2 = cards

    key = hand_key(c1, c2)

    in_position = state.in_position

    fold_rate = opponent.fold_rate()
    spr = state.spr

    # -------------------------
    # Base Probabilities
    # -------------------------

    if key in STRONG_RANGE:

        raise_prob = 1.0
        call_prob = 0.0

    elif key in MEDIUM_RANGE:

        raise_prob = 0.75 if in_position else 0.55
        call_prob = 0.25

    elif key in PLAYABLE_RANGE:

        raise_prob = 0.55 if in_position else 0.30
        call_prob = 0.35

    elif key in SPECULATIVE_RANGE:

        raise_prob = 0.40 if in_position else 0.20
        call_prob = 0.40

    else:  # Trash

        raise_prob = 0.15 if in_position else 0.05
        call_prob = 0.25 if in_position else 0.10

    # -------------------------
    # Opponent Adjustment
    # -------------------------

    # If opponent folds a lot → raise more
    raise_prob += fold_rate * 0.25

    # Clamp
    raise_prob = min(max(raise_prob, 0), 1)

    # -------------------------
    # Stack Depth Adjustment
    # -------------------------

    if spr <= 3:
        # shallow → aggression increases
        raise_prob += 0.10

    elif spr >= 10:
        # deep → speculative better
        call_prob += 0.05

    raise_prob = min(max(raise_prob, 0), 1)
    call_prob = min(max(call_prob, 0), 1)

    # -------------------------
    # Mixed Strategy Decision
    # -------------------------

    r = random.random()

    if r < raise_prob:
        return "RAISE"

    elif r < raise_prob + call_prob:
        return "CALL"

    return "FOLD"
