from treys import Card, Evaluator

evaluator = Evaluator()


def convert_card(card):
    """
    Convert from 'Ah' → treys integer format
    """
    return Card.new(card.rank + card.suit)


def evaluate_hand(my_cards, board_cards):
    """
    Returns hand strength score (lower is better in treys)
    """

    treys_hand = [convert_card(c) for c in my_cards]
    treys_board = [convert_card(c) for c in board_cards]

    score = evaluator.evaluate(treys_board, treys_hand)

    return score
