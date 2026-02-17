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
            return self.raise_or_call(state, win_prob)

        elif win_prob > 0.45:
            return self.call_or_check(state)

        else:
            return self.fold_or_check(state)

    # ---------- RAISE LOGIC ----------

    def raise_or_call(self, state, win_prob):

        for action in state.legal_actions:

            if action.startswith("RAISE"):

                parts = action.split(":")
                min_raise = int(parts[1])
                max_raise = int(parts[2])

                amount = self.compute_raise_amount(
                    state,
                    win_prob,
                    min_raise,
                    max_raise
                )

                return f"RAISE:{amount}"

        # If raise not available → call
        for action in state.legal_actions:
            if action.startswith("CALL"):
                return "CALL"

        return choose_safe_action(state.legal_actions)

    def compute_raise_amount(self, state, win_prob, min_raise, max_raise):

        pot = state.pot

        # Stronger hand → larger raise
        if win_prob > 0.9:
            target = int(pot * 1.5)

        elif win_prob > 0.75:
            target = int(pot * 1.0)

        elif win_prob > 0.6:
            target = int(pot * 0.6)

        else:
            target = min_raise

        # Clamp inside legal range
        target = max(min_raise, min(target, max_raise))

        return target

    # ---------- MEDIUM STRENGTH ----------

    def call_or_check(self, state):

        for action in state.legal_actions:
            if action.startswith("CALL"):
                return "CALL"

        for action in state.legal_actions:
            if action.startswith("CHECK"):
                return "CHECK"

        return choose_safe_action(state.legal_actions)

    # ---------- WEAK HAND ----------

    def fold_or_check(self, state):

        for action in state.legal_actions:
            if action.startswith("CHECK"):
                return "CHECK"

        for action in state.legal_actions:
            if action.startswith("FOLD"):
                return "FOLD"

        return choose_safe_action(state.legal_actions)
