RANK_ORDER = "23456789TJQKA"


def card_rank(card):
    return card[0]


def is_pair(c1, c2):
    return card_rank(c1) == card_rank(c2)


def suited(c1, c2):
    return c1[1] == c2[1]


def hand_key(c1, c2):
    r1 = card_rank(c1)
    r2 = card_rank(c2)

    # sort ranks descending
    if RANK_ORDER.index(r1) > RANK_ORDER.index(r2):
        high, low = r1, r2
    else:
        high, low = r2, r1

    if is_pair(c1, c2):
        return high + low

    if suited(c1, c2):
        return high + low + "s"

    return high + low + "o"


# --------------------------
# Position based ranges
# --------------------------

# Button (in position) — wider
BUTTON_RAISE = {
    "AA","KK","QQ","JJ","TT",
    "AKs","AQs","AJs","ATs",
    "KQs","KJs","QJs","JTs",
    "AKo","AQo","AJo",
    "99","88","77","66",
    "A9s","A8s","A7s",
    "KTs","QTs","J9s","T9s",
    "98s","87s"
}

# Out of position — tighter
BLIND_RAISE = {
    "AA","KK","QQ","JJ","TT",
    "AKs","AQs","AJs",
    "KQs","QJs",
    "AKo",
    "99","88","77"
}


def preflop_decision(cards, in_position):

    c1, c2 = cards
    key = hand_key(c1, c2)

    if in_position:
        if key in BUTTON_RAISE:
            return "RAISE"
        else:
            return "FOLD"

    else:
        if key in BLIND_RAISE:
            return "RAISE"
        else:
            return "FOLD"
