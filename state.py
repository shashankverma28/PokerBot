class GameState:
    def __init__(self):
        self.bankroll = 0
        self.hand_id = 0

        self.my_cards = []
        self.board_cards = []

        self.pot = 0
        self.legal_actions = []
        self.in_position = True

        self.my_stack = 0
        self.opp_stack = 0
        self.effective_stack = 0
        self.spr = 0.0


    def reset_hand(self):
        self.my_cards = []
        self.board_cards = []
        self.pot = 0
        self.legal_actions = []

    def update_spr(self):

        self.effective_stack = min(self.my_stack, self.opp_stack)

        if self.pot > 0:
            self.spr = self.effective_stack / self.pot
        else:
            self.spr = 0
