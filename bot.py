import sys

from state import GameState
from parser import parse_getaction
from strategy import Strategy
from cards import parse_cards
from opponent import OpponentModel



class PokerBot:
    def __init__(self):
        self.state = GameState()
        self.opponent = OpponentModel()
        self.strategy = Strategy()

    def handle_newgame(self, tokens):
        pass

    def handle_newhand(self, tokens):
        self.state.hand_id += 1
        self.state.reset_hand()

        button = int(tokens[2])

        # Heads-up:
        # button == 1 → we are dealer → in position
        # button == 0 → opponent dealer → out of position
        self.state.in_position = (button == 1)

        # Example: tokens contain hole cards at fixed positions
        # Adjust indices based on engine spec
        hole_cards = tokens[3:5]

        self.state.my_cards = parse_cards(hole_cards)
        self.state.my_stack = int(tokens[5])
        self.state.opp_stack = int(tokens[6])


    def handle_getaction(self, line):

        data = parse_getaction(line)

        # Update state from engine info
        self.state.pot = data["pot"]
        self.state.board_cards = parse_cards(data["board_cards"])
        self.state.legal_actions = data["legal_actions"]

        self.state.update_spr()

        # Update opponent model with last actions
        self.opponent.update(data["last_actions"])

        # Decide action using strategy
        action = self.strategy.decide(self.state, self.opponent)

        print(action)
        sys.stdout.flush()


    def handle_handover(self, tokens):
        pass

    def run(self):
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            tokens = line.split()
            command = tokens[0]

            if command == "NEWGAME":
                self.handle_newgame(tokens)

            elif command == "NEWHAND":
                self.handle_newhand(tokens)

            elif command == "GETACTION":
                self.handle_getaction(line)

            elif command == "HANDOVER":
                self.handle_handover(tokens)

            elif command == "REQUESTKEYVALUES":
                print("FINISH")
                sys.stdout.flush()


if __name__ == "__main__":
    bot = PokerBot()
    bot.run()
