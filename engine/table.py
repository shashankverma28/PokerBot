# engine/table.py

from engine.game_state import GameState


class Table:
    def __init__(self, num_players=6, starting_stack=1000):
        self.state = GameState(num_players, starting_stack)

    def start_new_hand(self):
        self.state.reset_for_new_hand()
        self.post_blinds()

    def post_blinds(self, small_blind=5, big_blind=10):
        sb_seat = (self.state.button_seat + 1) % self.state.num_players
        bb_seat = (self.state.button_seat + 2) % self.state.num_players

        sb_player = self.state.players[sb_seat]
        bb_player = self.state.players[bb_seat]

        self.state.pot += sb_player.post_blind(small_blind)
        self.state.pot += bb_player.post_blind(big_blind)

    def next_button(self):
        self.state.rotate_button()