def parse_getaction(line):
    parts = line.strip().split()

    pot = int(parts[1])
    num_board = int(parts[2])

    board_cards = parts[3:3+num_board]

    # find legal actions near end
    num_legal = int(parts[-2])
    legal_actions = parts[-num_legal:]

    return {
        "pot": pot,
        "board_cards": board_cards,
        "legal_actions": legal_actions
    }
