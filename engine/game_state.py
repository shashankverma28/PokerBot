# engine/game_state.py

from engine.player import Player


class GameState:
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

        self.current_actor = None

    # -----------------------------
    # POSITION LOGIC
    # -----------------------------

    def get_position_index(self, seat_id):
        return (seat_id - self.button_seat) % self.num_players

    def get_active_players(self):
        return [p for p in self.players if p.in_hand]

    def get_num_active_players(self):
        return len(self.get_active_players())

    def rotate_button(self):
        self.button_seat = (self.button_seat + 1) % self.num_players

    # -----------------------------
    # HAND CONTROL
    # -----------------------------

    def reset_for_new_hand(self):
        self.pot = 0
        self.board = []
        self.street = "preflop"

        for player in self.players:
            player.reset_for_new_hand()

    def collect_bets_to_pot(self):
        for player in self.players:
            self.pot += player.current_bet
            player.current_bet = 0