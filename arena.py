from pypokerengine.api.game import setup_config, start_poker

from pypoker_bot import MyPokerBot
from tournament_titan import TournamentTitan   # change opponent here


MAX_ROUNDS = 100
INITIAL_STACK = 1000
SMALL_BLIND = 5


config = setup_config(
    max_round=MAX_ROUNDS,
    initial_stack=INITIAL_STACK,
    small_blind_amount=SMALL_BLIND
)

config.register_player(name="Me", algorithm=MyPokerBot())
config.register_player(name="Opponent", algorithm=TournamentTitan()) #here aswell

game_result = start_poker(config, verbose=0)


# ----------- ANALYSIS -----------

players = game_result["players"]

me_stack = next(p["stack"] for p in players if p["name"] == "Me")
opp_stack = next(p["stack"] for p in players if p["name"] == "Opponent")

net_profit = me_stack - INITIAL_STACK

bb_per_100 = (net_profit / SMALL_BLIND) / MAX_ROUNDS * 100

print("\n========== MATCH SUMMARY ==========")
print(f"Total Hands: {MAX_ROUNDS}")
print(f"My Final Stack: {me_stack}")
print(f"Opponent Final Stack: {opp_stack}")
print(f"Net Profit: {net_profit}")
print(f"BB/100: {bb_per_100:.2f}")

if me_stack > opp_stack:
    print("Winner: Me")
elif me_stack < opp_stack:
    print("Winner: Opponent")
else:
    print("Result: Tie")

print("===================================")