from actions import choose_safe_action


class Strategy:
    def decide(self, state):
        return choose_safe_action(state.legal_actions)
