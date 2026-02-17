def parse_getaction(line):

    parts = line.strip().split()

    index = 1

    # Pot size
    pot = int(parts[index])
    index += 1

    # Board cards
    num_board = int(parts[index])
    index += 1

    board_cards = parts[index:index + num_board]
    index += num_board

    # Last actions (skip for now)
    num_last = int(parts[index])
    index += 1

    last_actions = parts[index:index + num_last]
    index += num_last

    # Legal actions
    num_legal = int(parts[index])
    index += 1

    legal_actions = parts[index:index + num_legal]
    index += num_legal

    # Timebank (optional)
    timebank = float(parts[index]) if index < len(parts) else 0.0

    return {
        "pot": pot,
        "board_cards": board_cards,
        "legal_actions": legal_actions,
        "last_actions": last_actions,
        "timebank": timebank
    }
