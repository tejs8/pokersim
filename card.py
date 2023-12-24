from cardmappings import mappings

class Card:
    """
    Card class, default set to Ace of Spades. 
    """
    rank = 'A'
    suit = 'S'
    val = 14

    def __init__(self, rank, suit):
        """
        Initializes card to set rank and suit. Also sets val attribute 
        to relevant value through mapping dictionary.
        """
        self.rank = rank
        self.suit = suit
        self.val = mappings[rank]
    
    def __str__(self,):
        """
        Prints  card characteristics, rank and suit.
        """
        return (f"{self.rank}{self.suit}")

    def __lt__(self, other):
        """
        Comparison method, compares cards by val attribute.
        """
        return self.val < other.val

    def __eq__(self, other):
        """
        Equality method to see if two cards are equal in suit and rank.
        """
        return isinstance(other, Card) and self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        """
        Hash method, needed for using cards in dicts and sets.
        """
        return hash((self.rank, self.suit))
    
    # Note: used to have __repr__ method, may not be needed.
    def __repr__(self,):
        return (f"{self.rank}{self.suit}")
    