from card import *

class Player:
    """
    Player object. Has option to be instantiated with given holecards,
    if not specified, random holding will be given to player.
    """

    def __init__(self, name, holecards = None):
        """
        Initialiation method for player. Optional holecards parameter.
        """
        self.name = name 
        if not holecards:
            self.hole_cards_set = False
            self.hole_cards = []
        else:
            self.hole_cards_set = True
            self.hole_cards = []
            self.hole_cards.append(Card(holecards[0][0], holecards[0][1]))
            self.hole_cards.append(Card(holecards[1][0], holecards[1][1]))
        self.hand = None
        self.handstrength = None

    def reset(self):
        """
        Resets player to be ready for another sim run.
        """
        if not self.hole_cards_set:
            self.hole_cards = []
        self.hand = None 
        self.handstrength = None
    
    def add_hand(self, hand, output = False):
        """
        Updates player's hand with board.
        """
        self.hand = hand.copy()
        self.hand.sort(reverse=True)
        self.hand_check(output)

    def hand_check(self, output):
        """
        Checks strength of player's hand.
        """
        # First check if player has a flush, straight, or straight flush:
        strength, val = self.non_pair_check()

        ranks = {}
        for card in self.hand:
            if card.rank not in ranks:
                ranks[card.rank] = 1
            else:
                ranks[card.rank]+=1

        # Straight flush
        if strength == "SF":
            self.handstrength = ("StraightFlush", 9, val)
            if output:
                if val != 14:
                    print(f"Player {self.num} has a {mappings[val]} high straight flush!")
                else:
                    print(f"Player {self.num} has a ROYAL FLUSH!!!")
            return
            
        # Quads
        if max(ranks.values()) == 4:
            quad = max(ranks, key = ranks.get)
            truehand = [mappings[quad]]
            i = 0
            while self.hand[i].rank == quad:
                i+=1
            truehand.append(self.hand[i].val)
            self.handstrength = ("Quads", 8, truehand)
            if output:
                print(f"Player {self.num} has quads with {mappings[quad]}s")
            return
        
        # Fullhouse check
        elif 3 in ranks.values():
            boat = False
            if 2 in ranks.values():
                boat = True
                triprank = key_lookup(ranks,3)
                pairrank = key_lookup(ranks,2)
            elif list(ranks.values()).count(3) > 1:
                boat = True
                triprank = key_lookup(ranks, 3)
                del ranks[triprank]
                pairrank = key_lookup(ranks,3)
            if boat:
                self.handstrength = ("FullHouse", 7, (mappings[triprank], mappings[pairrank]))
                if output:
                    print(f"Player {self.num} has {triprank}s full")
                return
            
        # Need to check for flush or straight
        if strength == "F":
            self.handstrength = ("Flush", 6, val)
            if output:
                print(f"Player {self.num} has a {mappings[val[0]]} high flush")
            return
        
        # Straight check:
        if strength == "S":
            self.handstrength = ("Straight", 5, val)
            if output:
                print(f"Player {self.num} has a {mappings[val]} high straight")
            return 
        
        if 3 in ranks.values():
            triprank = key_lookup(ranks, 3)
            first = key_lookup(ranks, 1)
            del ranks[first]
            second = key_lookup(ranks, 1)
            del ranks[second]
            truehand = [mappings[triprank], mappings[first], mappings[second]]
            if output:
                print(f"Player {self.num} has trip {triprank}s")
            self.handstrength = ("Trips", 4, truehand)
            return
        
        elif 2 in ranks.values() and list(ranks.values()).count(2) > 1:
            pairrank1 = key_lookup(ranks, 2)
            del ranks[pairrank1]
            pairrank2 = key_lookup(ranks,2)
            del ranks[pairrank2]

            if 2 in ranks.values():
                pot_high = key_lookup(ranks, 2)
                high = key_lookup(ranks, 1)
                true_high = pot_high if mappings[pot_high] > mappings[high] else high
            else:
                true_high = key_lookup(ranks, 1)
            
            truehand = [mappings[pairrank1], mappings[pairrank2], mappings[true_high]]

            if output:
                print(f"Player {self.num} has two pair: {pairrank1}s and {pairrank2}s")

            self.handstrength = ("TwoPair", 3, truehand)
            return

        elif 2 in ranks.values():
            pairrank = key_lookup(ranks, 2)
            first = key_lookup(ranks, 1)
            del ranks[first] 
            second = key_lookup(ranks, 1)
            del ranks[second]
            third = key_lookup(ranks, 1)
            del ranks[third]
            truehand = [mappings[pairrank], mappings[first], mappings[second], mappings[third]]
            if output:
                print(f"Player {self.num} has a pair of {pairrank}s")
            self.handstrength = ("Pair", 2, truehand)
            return
        
        else:
            truehand = []
            for i in range(5):
                high = key_lookup(ranks, 1)
                del ranks[high]
                truehand.append(mappings[high])
            if output:
                print(f"Player {self.num} has a high card of {truehand[0]}")
            self.handstrength = ("HighCard", 1, truehand)
            return
    
    def hand_compare(self, other):
        """
        Methid to compare hand strengths of two players
        """
        
        if self.handstrength[1] != other.handstrength[1]:
            return -1 if self.handstrength[1] < other.handstrength[1] else 1
        
        # Straight flush and straight comp
        if self.handstrength[1] == 9 or self.handstrength[1] == 5:
            if self.handstrength[2] == other.handstrength[2]: return 0
            elif self.handstrength[2] < other.handstrength[2]: return -1
            else: return 1

        # Everything else
        else:
            for i in range(len(self.handstrength[2])):
                try:
                    if self.handstrength[2][i] > other.handstrength[2][i]: return 1
                    elif self.handstrength[2][i] < other.handstrength[2][i]: return -1
                except:
                    stop = "here"
            return 0
            
    def non_pair_check(self):
        """
        Method to check if player has a hand strength that is not built off of having
        cards of the same rank- this includes flush, straight, and straight flush.
        """
        suits, flushsuit = {}, 0
        flushhand = []
        flush = False
        for card in self.hand:
            if card.suit not in suits:
                suits[card.suit] = 1
            else:
                suits[card.suit]+=1

        # Player has a flush at the very least:
        if max(suits.values()) >= 5:
            flush = True
            flushsuit = max(suits, key=suits.get)

            # Add all flush cards to an array
            for card in self.hand:
                if card.suit == flushsuit:
                    flushhand.append(card.val)
            
            """
            Important: need to check if first value in flush hand
            is an Ace. If so we append 1 to the end of the array.
            Since array is in reverse order, this will help us with
            the edge case of player having a 5 high straight.
            """ 
            if flushhand[0] == 14: flushhand.append(1)

            # Check for the straight flush
            pot_straight = straight_check(flushhand)
            if pot_straight != -1:
                return ('SF', pot_straight)
            return ('F', flushhand)
        
        # Player does not have a flush, now check for straights
        straighthand = []
        for card in self.hand:
            straighthand.append(card.val)

        # Need to append 1 for the same reason as before, so we
        # don't miss a "wheel" straight (5 high straight)
        if straighthand[0] == 14: straighthand.append(1)

        pot_straight = straight_check(straighthand)

        if pot_straight != -1:
            return('S', pot_straight)
            
        # Don't have anything
        return ('N', 0)

def straight_check(card_sequence):
    """
    Helper function, given a sequence of cards, checks if 
    5 consecutive cards exist in the sequence. If so, will 
    return the value of highest card in that sequence. If 
    not, will return -1.
    """
    consec, pot_straight = 0, 0
    for idx, val in enumerate(card_sequence[:-1]):
        if val == card_sequence[idx+1] + 1:
            if consec == 0:
                pot_straight = val 
            consec+=1
        elif val == card_sequence[idx+1]: continue
        else:
            consec, pot_straight = 0,0
        if consec >= 4:
            return pot_straight
            
    # Don't have anything
    return -1


def key_lookup(dict, search):
    for key, val in dict.items():
        if val == search:
            return key