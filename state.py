class GameState:
    def __init__(self):
        self.bankroll = 0
        self.hand_id = 0

        self.my_cards = []
        self.board_cards = []

        self.pot = 0
        self.legal_actions = []
        self.in_position = True

    def reset_hand(self):
        self.my_cards = []
        self.board_cards = []
        self.pot = 0
        self.legal_actions = []
