# preflop.py

RANK_ORDER = "23456789TJQKA"


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


# ----------------------------------
# Simple Preflop Range (baseline)
# ----------------------------------

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


def preflop_decision(cards, in_position):

    c1, c2 = cards

    key = hand_key(c1, c2)

    # ---------- Strong Hands ----------
    if key in STRONG_RANGE:
        return "RAISE"

    # ---------- Medium Hands ----------
    if key in MEDIUM_RANGE:

        if in_position:
            return "RAISE"
        else:
            return "CALL"

    # ---------- Weak Hands ----------
    if in_position:
        return "CALL"

    return "FOLD"
