from pypokerengine.players import BasePokerPlayer

from strategy import Strategy
from opponent import OpponentModel
from state import GameState


class MyPokerBot(BasePokerPlayer):

    def __init__(self):
        super().__init__()
        self.strategy = Strategy()
        self.opponent = OpponentModel()

    # Engine entry point
    def declare_action(self, valid_actions, hole_card, round_state):

        state = self._convert_state(valid_actions, hole_card, round_state)

        action = self.strategy.decide(state, self.opponent)

        return self._convert_action(action, valid_actions)

    # Convert PyPokerEngine state to your GameState
    def _convert_state(self, valid_actions, hole_card, round_state):

        from cards import parse_cards

        state = GameState()

        # Convert card format (e.g. "SA" -> "As")
        def convert_card_format(card_str):
            suit = card_str[0].lower()
            rank = card_str[1].upper()
            return rank + suit

        converted_hole = [convert_card_format(c) for c in hole_card]
        converted_board = [convert_card_format(c) for c in round_state["community_card"]]

        state.my_cards = parse_cards(converted_hole)
        state.board_cards = parse_cards(converted_board)

        # Pot size
        state.pot = round_state["pot"]["main"]["amount"]

        # Convert legal actions to your format
        converted_actions = []

        for action in valid_actions:

            name = action["action"]

            if name == "fold":
                converted_actions.append("FOLD")

            elif name == "call":
                amount = action["amount"]
                if amount == 0:
                    converted_actions.append("CHECK")
                else:
                    converted_actions.append(f"CALL:{amount}")

            elif name == "raise":
                min_raise = action["amount"]["min"]
                max_raise = action["amount"]["max"]
                converted_actions.append(f"RAISE:{min_raise}:{max_raise}")

        state.legal_actions = converted_actions

        # Determine position (heads-up assumption)
        seats = round_state["seats"]

        hero_index = next(
            i for i, s in enumerate(seats)
            if s["uuid"] == self.uuid
        )

        state.in_position = (hero_index == len(seats) - 1)

        # Stack sizes (heads-up only)
        hero_seat = seats[hero_index]
        state.my_stack = hero_seat["stack"]

        opponent_seat = next(
            s for s in seats
            if s["uuid"] != self.uuid
        )

        state.opp_stack = opponent_seat["stack"]

        # Compute SPR
        state.update_spr()

        return state

    # Convert your action string to engine format
    def _convert_action(self, action, valid_actions):

        action = action.upper()

        # Fold
        if action == "FOLD":
            return "fold", 0

        # Call or check
        if action == "CALL" or action == "CHECK":
            call_action = next(a for a in valid_actions if a["action"] == "call")
            return "call", call_action["amount"]

        # Raise
        if action.startswith("RAISE"):

            raise_action = next(
                a for a in valid_actions if a["action"] == "raise"
            )

            min_raise = raise_action["amount"]["min"]
            max_raise = raise_action["amount"]["max"]

            try:
                desired_amount = int(action.split(":")[1])
            except:
                desired_amount = min_raise

            amount = max(min_raise, min(desired_amount, max_raise))

            return "raise", amount

        # Fallback
        return "fold", 0

    # Required engine methods
    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass