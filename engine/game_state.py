# engine/game_state.py

from .player import Player


class GameState:
    POSITION_NAMES = ["BTN", "SB", "BB", "UTG", "HJ", "CO"]

    def __init__(self, num_players=6, starting_stack=1000):
        self.num_players = num_players
        self.players = [
            Player(seat_id=i, starting_stack=starting_stack)
            for i in range(num_players)
        ]

        self.hero_seat = 0
        self.button_seat = 0

        self.pot = 0
        self.board = []
        self.street = "preflop"

        self.current_actor_index = None
        self.last_raiser_index = None

    # -----------------------------
    # POSITION LOGIC
    # -----------------------------

    def get_position_index(self, seat_id):
        return (seat_id - self.button_seat) % self.num_players

    def get_position_name(self, seat_id):
        index = self.get_position_index(seat_id)
        return self.POSITION_NAMES[index]

    def rotate_button(self):
        self.button_seat = (self.button_seat + 1) % self.num_players

    # -----------------------------
    # ACTIVE PLAYERS
    # -----------------------------

    def get_active_players(self):
        return [p for p in self.players if p.in_hand]

    def get_active_seat_indices(self):
        return [p.seat_id for p in self.players if p.in_hand]

    def get_num_active_players(self):
        return len(self.get_active_players())

    # -----------------------------
    # HAND RESET
    # -----------------------------

    def reset_for_new_hand(self):
        self.pot = 0
        self.board = []
        self.street = "preflop"
        self.current_actor_index = None
        self.last_raiser_index = None

        for player in self.players:
            player.reset_for_new_hand()

    # -----------------------------
    # ACTION ORDER LOGIC
    # -----------------------------

    def get_preflop_action_order(self):
        """
        Preflop order starts from UTG (first seat after BB)
        """
        bb_seat = (self.button_seat + 2) % self.num_players
        first_to_act = (bb_seat + 1) % self.num_players

        order = []
        current = first_to_act

        while True:
            if self.players[current].in_hand:
                order.append(current)

            current = (current + 1) % self.num_players
            if current == first_to_act:
                break

        return order

    def get_postflop_action_order(self):
        """
        Postflop starts from SB (first seat after button)
        """
        first_to_act = (self.button_seat + 1) % self.num_players

        order = []
        current = first_to_act

        while True:
            if self.players[current].in_hand:
                order.append(current)

            current = (current + 1) % self.num_players
            if current == first_to_act:
                break

        return order

    # -----------------------------
    # BETTING ROUND CONTROL
    # -----------------------------

    def start_betting_round(self):
        if self.street == "preflop":
            order = self.get_preflop_action_order()
        else:
            order = self.get_postflop_action_order()

        self.current_actor_index = 0
        self.action_order = order
        self.last_raiser_index = None

    def get_current_actor(self):
        if self.current_actor_index is None:
            return None

        if self.current_actor_index >= len(self.action_order):
            return None

        seat = self.action_order[self.current_actor_index]
        return self.players[seat]

    def move_to_next_actor(self):
        self.current_actor_index += 1

    def betting_round_complete(self):
        if self.last_raiser_index is None:
            return self.current_actor_index >= len(self.action_order)
        return (
            self.current_actor_index >= len(self.action_order)
            and self.action_order[-1] == self.last_raiser_index
        )