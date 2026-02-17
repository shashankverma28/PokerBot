import sys

from actions import choose_safe_action
from evaluator import evaluate_hand
from montecarlo import estimate_win_probability


class Strategy:

    def decide(self, state):

        # Safety fallback
        if not state.my_cards:
            return choose_safe_action(state.legal_actions)

        # ----- Hand Evaluation -----
        score = evaluate_hand(state.my_cards, state.board_cards)

        win_prob = estimate_win_probability(
            state.my_cards,
            state.board_cards,
            simulations=300
        )

        # ----- Decision Logic -----
        if win_prob > 0.75 or score < 2500:
            return self.raise_or_call(state)

        elif win_prob > 0.45:
            return self.call_or_check(state)

        else:
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
