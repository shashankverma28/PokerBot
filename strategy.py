from actions import choose_safe_action
from evaluator import evaluate_hand


class Strategy:

    def decide(self, state):

        # If we don't have cards yet, fallback
        if not state.my_cards:
            return choose_safe_action(state.legal_actions)

        score = evaluate_hand(state.my_cards, state.board_cards)

        # Simple rule-based logic (temporary)
        if score < 3000:
            # strong hand
            return self.raise_or_call(state)

        elif score < 6000:
            # medium hand
            return choose_safe_action(state.legal_actions)

        else:
            # weak hand
            return self.fold_or_check(state)

    def raise_or_call(self, state):

        for action in state.legal_actions:
            if action.startswith("RAISE"):
                parts = action.split(":")
                min_raise = int(parts[1])
                return f"RAISE:{min_raise}"

        for action in state.legal_actions:
            if action.startswith("CALL"):
                return "CALL"

        return choose_safe_action(state.legal_actions)

    def fold_or_check(self, state):

        for action in state.legal_actions:
            if action.startswith("CHECK"):
                return "CHECK"

        for action in state.legal_actions:
            if action.startswith("FOLD"):
                return "FOLD"

        return choose_safe_action(state.legal_actions)
