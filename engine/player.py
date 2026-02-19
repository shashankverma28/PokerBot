# engine/player.py

from engine.player_stats import PlayerStats

class Player:
    def __init__(self, seat_id, starting_stack):
        self.seat_id = seat_id
        self.stack = starting_stack
        self.hole_cards = []
        self.in_hand = True
        self.current_bet = 0
        self.stats = PlayerStats()

    def reset_for_new_hand(self):
        self.hole_cards = []
        self.in_hand = True
        self.current_bet = 0

    def post_blind(self, amount):
        blind = min(amount, self.stack)
        self.stack -= blind
        self.current_bet += blind
        return blind

    def bet(self, amount):
        bet_amount = min(amount, self.stack)
        self.stack -= bet_amount
        self.current_bet += bet_amount
        return bet_amount

    def fold(self):
        self.in_hand = False