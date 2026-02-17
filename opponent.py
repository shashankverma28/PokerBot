class OpponentModel:

    def __init__(self):
        self.total_actions = 0
        self.folds = 0
        self.calls = 0
        self.raises = 0

    def update(self, last_actions):

        for action in last_actions:

            if "FOLD" in action:
                self.folds += 1

            elif "CALL" in action:
                self.calls += 1

            elif "RAISE" in action:
                self.raises += 1

            self.total_actions += 1

    # ---------- Stats ----------

    def fold_rate(self):

        if self.total_actions == 0:
            return 0.3   # default assumption

        return self.folds / self.total_actions

    def aggression(self):

        if self.total_actions == 0:
            return 0.5

        return self.raises / self.total_actions
