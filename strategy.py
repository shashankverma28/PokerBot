import sys
import random

from actions import choose_safe_action
from evaluator import evaluate_hand
from montecarlo import estimate_win_probability
from preflop import preflop_decision
from draws import detect_draw
from board_texture import classify_board

class Strategy:

    def decide(self, state, opponent):

        if not state.my_cards:
            return choose_safe_action(state.legal_actions)

        in_pos = state.in_position

        # ---------- Preflop Logic ----------

        if len(state.board_cards) == 0:

            action = preflop_decision(state.my_cards, state.in_position)

            print(f"[DEBUG] Preflop Action: {action}", file=sys.stderr)

            if action == "RAISE":
                return self.raise_or_call(state, 0.7)

            if action == "FOLD":
                return self.fold_or_check(state)

            # fallback
            return self.call_or_check(state)


        else:

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

        # ---------- Board Texture ----------

        board_info = classify_board(state.board_cards)
        texture = board_info["texture"]
        wet_board = board_info["wet"]

        print(f"[DEBUG] Texture: {texture}", file=sys.stderr)
        print(f"[DEBUG] In Position: {in_pos}", file=sys.stderr)
        print(f"[DEBUG] Win Prob: {win_prob:.3f}", file=sys.stderr)
        print(f"[DEBUG] Pot Odds: {pot_odds:.3f}", file=sys.stderr)
        print(f"[DEBUG] Opp Fold Rate: {fold_rate:.2f}", file=sys.stderr)

        # ---------- Strong Hand Threshold ----------

        strong_threshold = 0.75

        # Texture adjustment
        if texture in {"wet_heavy", "connected"}:
            strong_threshold += 0.07

        elif texture in {"monotone", "two_tone"}:
            strong_threshold += 0.04

        elif texture == "dry_high":
            strong_threshold -= 0.05

        elif texture == "paired":
            strong_threshold -= 0.03

        # Position adjustment
        if in_pos:
            strong_threshold -= 0.05
        else:
            strong_threshold += 0.05


        if win_prob > strong_threshold or (score is not None and score < 2500):
            return self.raise_or_call(state, win_prob)

        # ---------- Medium Strength Value Raise ----------

        medium_lower = 0.60
        medium_upper = 0.75

        if medium_lower <= win_prob < medium_upper:

            value_raise_prob = 0.3 + fold_rate * 0.4
            value_raise_prob *= (1 - aggression * 0.3)

            # POSITION ADJUSTMENT
            if in_pos:
                value_raise_prob += 0.15
            else:
                value_raise_prob -= 0.15

            value_raise_prob = max(0.0, min(value_raise_prob, 0.8))

            print(f"[DEBUG] Value Raise Prob: {value_raise_prob:.2f}", file=sys.stderr)

            if random.random() < value_raise_prob:
                return self.raise_or_call(state, win_prob)

            return self.call_or_check(state)

        # ---------- Adaptive Bluff + Semi Bluff ----------

        draw_info = detect_draw(state.my_cards, state.board_cards)
        has_draw = draw_info["any_draw"]

        base_bluff = 0.4
        bluff_chance = base_bluff * fold_rate
        bluff_chance *= (1 - aggression * 0.5)

        # Prefer bluff when draw present
        if has_draw:
            bluff_chance *= 1.5
        else:
            bluff_chance *= 0.6

        # Position adjustment
        if in_pos:
            bluff_chance *= 1.3
        else:
            bluff_chance *= 0.7
            
        # Texture adjustment
        if texture in {"dry_high", "paired"}:
            bluff_chance *= 1.3

        elif texture in {"wet_heavy", "connected"}:
            bluff_chance *= 0.6

        elif texture == "monotone":
            bluff_chance *= 1.1

        bluff_chance = max(0.0, min(bluff_chance, 0.8))

        print(f"[DEBUG] Bluff Chance: {bluff_chance:.2f}", file=sys.stderr)
        print(f"[DEBUG] Has Draw: {has_draw}", file=sys.stderr)

        if win_prob < 0.45 and random.random() < bluff_chance:
            return self.bluff_raise(state)

        # ---------- Normal EV Decision ----------

        if call_amount > 0:
            if win_prob > pot_odds:
                return self.call_or_check(state)
            else:
                return self.fold_or_check(state)

        return self.call_or_check(state)

    # ---------- Helpers ----------

    def bluff_raise(self, state):

        for action in state.legal_actions:
            if action.startswith("RAISE"):

                parts = action.split(":")
                min_raise = int(parts[1])
                max_raise = int(parts[2])

                amount = int(min_raise * 1.2)
                amount = max(min_raise, min(amount, max_raise))

                return f"RAISE:{amount}"

        return self.call_or_check(state)

    def compute_pot_odds(self, pot, call_amount):

        if call_amount == 0:
            return 0

        return call_amount / (pot + call_amount)

    def get_call_amount(self, state):

        for action in state.legal_actions:
            if action.startswith("CALL"):
                parts = action.split(":")
                return int(parts[1])

        return 0

    def raise_or_call(self, state, win_prob):

        for action in state.legal_actions:
            if action.startswith("RAISE"):

                parts = action.split(":")
                min_raise = int(parts[1])
                max_raise = int(parts[2])

                target = int(state.pot * 1.2)
                amount = max(min_raise, min(target, max_raise))

                return f"RAISE:{amount}"

        return self.call_or_check(state)

    def call_or_check(self, state):

        for action in state.legal_actions:
            if action.startswith("CALL"):
                return action.split(":")[0]

        for action in state.legal_actions:
            if action.startswith("CHECK"):
                return "CHECK"

        return choose_safe_action(state.legal_actions)

    def fold_or_check(self, state):

        for action in state.legal_actions:
            if action.startswith("FOLD"):
                return "FOLD"

        return "CHECK"
