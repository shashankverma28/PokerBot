import random


def choose_safe_action(legal_actions):
    """
    Always returns a valid action.
    """

    # Prefer CHECK
    for action in legal_actions:
        if action.startswith("CHECK"):
            return "CHECK"

    # Prefer CALL
    for action in legal_actions:
        if action.startswith("CALL"):
            return "CALL"

    # Random fallback
    action = random.choice(legal_actions)

    if action.startswith("RAISE"):
        parts = action.split(":")
        min_raise = int(parts[1])
        max_raise = int(parts[2])

        amount = random.randint(min_raise, max_raise)
        return f"RAISE:{amount}"

    return action
