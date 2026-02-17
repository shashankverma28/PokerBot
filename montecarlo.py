import random
from treys import Card, Evaluator, Deck


evaluator = Evaluator()


def convert_card(card):
    return Card.new(card.rank + card.suit)


def estimate_win_probability(my_cards, board_cards, simulations=500):

    my_treys = [convert_card(c) for c in my_cards]
    board_treys = [convert_card(c) for c in board_cards]

    wins = 0
    ties = 0

    for _ in range(simulations):

        deck = Deck()

        # Remove known cards from deck
        for c in my_treys + board_treys:
            deck.cards.remove(c)

        # Opponent hole cards
        opp_cards = deck.draw(2)

        # Complete board
        remaining_board = 5 - len(board_treys)
        board_complete = board_treys + deck.draw(remaining_board)

        my_score = evaluator.evaluate(board_complete, my_treys)
        opp_score = evaluator.evaluate(board_complete, opp_cards)

        if my_score < opp_score:
            wins += 1
        elif my_score == opp_score:
            ties += 1

    win_rate = (wins + 0.5 * ties) / simulations

    return win_rate
