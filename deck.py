from card import Card 

def create_pack(remove_set = None):
    """
    Initializes a deck of cards. If no remove_set is specified, 
    all 52 cards are added to the deck. Otherwise, all cards except
    those specified in remove_set are added to deck.
    """
    deck = set()

    # Add cards:
    add_rank(deck, 'A')
    for i in range(2, 11):
        add_rank(deck, i)
    add_rank(deck, 'J')
    add_rank(deck, 'Q')
    add_rank(deck, 'K')

    if remove_set is not None:
        for card in remove_set:
            deck.remove(card)
    return list(deck)

def add_rank(deck, rank):
    """
    Helper function to add all suits of a specified
    rank to a given deck.
    """
    deck.add(Card(rank, 'S'))
    deck.add(Card(rank, 'H'))
    deck.add(Card(rank, 'C'))
    deck.add(Card(rank, 'D'))