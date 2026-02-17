import sys
import random

from actions import choose_safe_action
from evaluator import evaluate_hand
from montecarlo import estimate_win_probability


class Strategy:

    def decide(self, state, opponent):

        if not state.my_cards:
            return choose_safe_action(state.legal_actions)

        # ---------- Preflop vs Postflop ----------

        if len(state.board_cards) == 0:

            # Preflop: use Monte Carlo only
            win_prob = estimate_win_probability(
                state.my_cards,
                [],
                simulations=300
            )

            score = None  # not used preflop

        else:

            # Postflop: evaluator + Monte Carlo
            score = evaluate_hand(state.my_cards, state.board_cards)

            win_prob = estimate_win_probability(
                state.my_cards,
                state.board_cards,
                simulations=300
            )


        call_amount = self.get_call_amount(state)

        pot_odds = self.compute_pot_odds(state.pot, call_amount)

        fold_rate = opponent.fold_rate()
        aggression = opponent.aggression()

        print(f"[DEBUG] Win Prob: {win_prob:.3f}", file=sys.stderr)
        print(f"[DEBUG] Pot Odds: {pot_odds:.3f}", file=sys.stderr)
        print(f"[DEBUG] Opp Fold Rate: {fold_rate:.2f}", file=sys.stderr)


        # ---------- Strong Hand ----------
        if win_prob > 0.75 or (score is not None and score < 2500):
            return self.raise_or_call(state, win_prob)
        
        # ---------- Medium Strength Value Raise ----------

        medium_lower = 0.60
        medium_upper = 0.75

        if medium_lower <= win_prob < medium_upper:

            # More aggressive if opponent folds often
            value_raise_prob = 0.3 + opponent.fold_rate() * 0.4

            # Slight reduction vs aggressive opponents
            value_raise_prob *= (1 - opponent.aggression() * 0.3)

            value_raise_prob = max(0.0, min(value_raise_prob, 0.8))

            print(f"[DEBUG] Value Raise Prob: {value_raise_prob:.2f}", file=sys.stderr)

            if random.random() < value_raise_prob:
                print("[DEBUG] Medium Strength Raising", file=sys.stderr)
                return self.raise_or_call(state, win_prob)

            # Otherwise play passively
            return self.call_or_check(state)


        # ---------- Adaptive Bluff Opportunity ----------

        # Base bluff aggressiveness
        base_bluff = 0.4
        # Scale with opponent fold tendency
        bluff_chance = base_bluff * fold_rate
        # Reduce bluffing vs aggressive opponents
        bluff_chance *= (1 - aggression * 0.5)
        # Clamp safety
        bluff_chance = max(0.0, min(bluff_chance, 0.8))

        print(f"[DEBUG] Bluff Chance: {bluff_chance:.2f}", file=sys.stderr)

        if win_prob < 0.35 and random.random() < bluff_chance:

            print("[DEBUG] Bluffing!", file=sys.stderr)
            return self.bluff_raise(state)


        # ---------- Medium Hand ----------
        if call_amount > 0:
            if win_prob > pot_odds:
                return self.call_or_check(state)
            else:
                return self.fold_or_check(state)

        return self.call_or_check(state)

    # ---------- Bluff Raise ----------

    def bluff_raise(self, state):

        for action in state.legal_actions:
            if action.startswith("RAISE"):

                parts = action.split(":")
                min_raise = int(parts[1])
                max_raise = int(parts[2])

                #Smarter Bluff Size

                amount = int(min_raise * 1.2)
                amount = max(min_raise, min(amount, max_raise))

                return f"RAISE:{amount}"

        return self.call_or_check(state)

    # ---------- Pot Odds ----------

    def compute_pot_odds(self, pot, call_amount):

        if call_amount == 0:
            return 0

        return call_amount / (pot + call_amount)

    def get_call_amount(self, state):

        for action in state.legal_actions:
            if action.startswith("CALL"):

                parts = action.split(":")

                if len(parts) > 1:
                    return int(parts[1])

                return 0

        return 0

    # ---------- Value Raise ----------

    def raise_or_call(self, state, win_prob):

        for action in state.legal_actions:

            if action.startswith("RAISE"):

                parts = action.split(":")
                min_raise = int(parts[1])
                max_raise = int(parts[2])

                pot = state.pot

                if win_prob > 0.9:
                    target = int(pot * 1.5)
                else:
                    target = int(pot * 0.8)

                target = max(min_raise, min(target, max_raise))

                return f"RAISE:{target}"

        for action in state.legal_actions:
            if action.startswith("CALL"):
                return "CALL"

        return choose_safe_action(state.legal_actions)

    # ---------- Call / Check ----------

    def call_or_check(self, state):

        for action in state.legal_actions:
            if action.startswith("CALL"):
                return "CALL"

        for action in state.legal_actions:
            if action.startswith("CHECK"):
                return "CHECK"

        return choose_safe_action(state.legal_actions)

    # ---------- Fold / Check ----------

    def fold_or_check(self, state):

        for action in state.legal_actions:
            if action.startswith("CHECK"):
                return "CHECK"

        for action in state.legal_actions:
            if action.startswith("FOLD"):
                return "FOLD"

        return choose_safe_action(state.legal_actions)
