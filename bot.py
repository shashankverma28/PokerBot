import sys
import random


class PokerBot:
    def __init__(self):
        self.bankroll = 0
        self.hand_id = 0

    # ---------- ENGINE EVENTS ----------

    def handle_newgame(self, tokens):
        # NEWGAME player1 player2 stack bb numHands timeBank
        pass

    def handle_newhand(self, tokens):
        # NEWHAND handId button holecards myBank oppBank timeBank
        self.hand_id += 1

    def handle_handover(self, tokens):
        # HANDOVER ...
        pass

    # ---------- DECISION LOGIC ----------

    def choose_action(self, legal_actions):
        """
        legal_actions examples:
        ["FOLD", "CALL", "CHECK"]
        ["FOLD", "CALL", "RAISE:10:100"]
        """

        # Prefer CHECK if available (free action)
        for action in legal_actions:
            if action.startswith("CHECK"):
                return "CHECK"

        # Prefer CALL if available
        for action in legal_actions:
            if action.startswith("CALL"):
                return "CALL"

        # Otherwise pick random legal action
        action = random.choice(legal_actions)

        # Handle raise range
        if action.startswith("RAISE"):
            parts = action.split(":")
            min_raise = int(parts[1])
            max_raise = int(parts[2])

            amount = random.randint(min_raise, max_raise)
            return f"RAISE:{amount}"

        return action

    # ---------- GETACTION HANDLER ----------

    def handle_getaction(self, line):
        """
        GETACTION format varies by competition,
        but legal actions are always at the end.
        """

        parts = line.strip().split()

        try:
            num_legal = int(parts[-2])
        except:
            # fallback safety
            print("CHECK")
            sys.stdout.flush()
            return

        legal_actions = parts[-num_legal:]

        action = self.choose_action(legal_actions)

        print(action)
        sys.stdout.flush()

    # ---------- MAIN LOOP ----------

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
