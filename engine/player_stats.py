# engine/player_stats.py

class PlayerStats:
    def __init__(self):
        self.hands_played = 0
        self.vpip = 0
        self.pfr = 0
        self.aggression = 0
        self.fold_to_cbet = 0

        # internal counters
        self._vpip_count = 0
        self._pfr_count = 0
        self._bet_raise_count = 0
        self._call_count = 0

    def record_vpip(self):
        self._vpip_count += 1

    def record_pfr(self):
        self._pfr_count += 1

    def record_bet_or_raise(self):
        self._bet_raise_count += 1

    def record_call(self):
        self._call_count += 1

    def finalize_hand(self):
        self.hands_played += 1
        if self.hands_played > 0:
            self.vpip = self._vpip_count / self.hands_played
            self.pfr = self._pfr_count / self.hands_played

        if self._call_count > 0:
            self.aggression = self._bet_raise_count / self._call_count