import random

mappings = {
    2:2,
    3:3,
    4:4,
    5:5,
    6:6,
    7:7,
    8:8,
    9:9,
    10: 10,
    11: 'J',
    12: 'Q',
    13: 'K',
    14: 'A',
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

class Player:

    def __init__(self, name, holecards = None):
        self.name = name 
        if not holecards:
            self.hole_cards_set = False
            self.hole_cards = []
        else:
            self.hole_cards_set = True
            self.hole_cards.append(Card(holecards[0][0], holecards[0][1]))
            self.hole_cards.append(Card(holecards[1][0], holecards[1][1]))

    # Old init
    def __init__(self, num, hand, output=False):
        self.num = num
        self.hand = hand.copy()
        self.hand.sort(reverse=True)
        self.handstrength = None
        self.hand_check(hand, output)

    def hand_check(self, hand, output):
        ranks = {}
        for card in self.hand:
            if card.rank in ranks:
                ranks[card.rank]+=1
            else:
                ranks[card.rank] = 1
        
        # Check for straight flush, flush, and straight up here
        strength, val = non_pair_check(self.hand)

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
            while self.hand[i].val == quad:
                i+=1
            truehand.append(self.hand[i].val)
            self.handstrength = ("Quads", 8, truehand)
            if output:
                print(f"Player {self.num} has quads with {mappings[quad]}s")
            return
        
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
        stop = "here"
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
        

class Card:
    rank = 'A'
    suit = 'S'
    val = 0

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.val = mappings[rank]
    
    def __str__(self,):
        return (f"{self.rank}{self.suit}")
    
    def __repr__(self,):
        return (f"{self.rank}{self.suit}")
    
    def __lt__(self, other):
        return self.val < other.val

def create_pack(remove_set = set()):
    deck = []
    deck.append(Card('A', 'S'))
    deck.append(Card('A', 'H'))
    deck.append(Card('A', 'C'))
    deck.append(Card('A', 'D'))
    deck.append(Card(2, 'S'))
    deck.append(Card(2, 'H'))
    deck.append(Card(2, 'C'))
    deck.append(Card(2, 'D'))
    deck.append(Card(3, 'S'))
    deck.append(Card(3, 'H'))
    deck.append(Card(3, 'C'))
    deck.append(Card(3, 'D'))
    deck.append(Card(4, 'S'))
    deck.append(Card(4, 'H'))
    deck.append(Card(4, 'C'))
    deck.append(Card(4, 'D'))
    deck.append(Card(5, 'S'))
    deck.append(Card(5, 'H'))
    deck.append(Card(5, 'C'))
    deck.append(Card(5, 'D'))
    deck.append(Card(6, 'S'))
    deck.append(Card(6, 'H'))
    deck.append(Card(6, 'C'))
    deck.append(Card(6, 'D'))
    deck.append(Card(7, 'S'))
    deck.append(Card(7, 'H'))
    deck.append(Card(7, 'C'))
    deck.append(Card(7, 'D'))
    deck.append(Card(8, 'S'))
    deck.append(Card(8, 'H'))
    deck.append(Card(8, 'C'))
    deck.append(Card(8, 'D'))
    deck.append(Card(9, 'S'))
    deck.append(Card(9, 'H'))
    deck.append(Card(9, 'C'))
    deck.append(Card(9, 'D'))
    deck.append(Card(10, 'S'))
    deck.append(Card(10, 'H'))
    deck.append(Card(10, 'C'))
    deck.append(Card(10, 'D'))
    deck.append(Card('J', 'S'))
    deck.append(Card('J', 'H'))
    deck.append(Card('J', 'C'))
    deck.append(Card('J', 'D'))
    deck.append(Card('Q', 'S'))
    deck.append(Card('Q', 'H'))
    deck.append(Card('Q', 'C'))
    deck.append(Card('Q', 'D'))
    deck.append(Card('K', 'S'))
    deck.append(Card('K', 'H'))
    deck.append(Card('K', 'C'))
    deck.append(Card('K', 'D'))

    retdeck = [card for card in deck if (card.rank, card.suit) not in remove_set]
    return retdeck

def non_pair_check(hand):
    suits, flushsuit = {}, 0
    flushhand = []
    flush = False
    for card in hand:
        if card.suit not in suits:
            suits[card.suit] = 1
        else:
            suits[card.suit]+=1

    # Flush at the very least
    if max(suits.values()) >= 5:
        flushsuit = max(suits, key=suits.get)
        flush = True
        for card in hand:
            if card.suit == flushsuit:
                flushhand.append(card.val)
        if flushhand[0] == 14: flushhand.append(1)
        # Check for the straight flush
        consec, pot_straight = 0, 0
        for idx, val in enumerate(flushhand[:-1]):
            if val == flushhand[idx+1] + 1:
                if consec == 0:
                    pot_straight = val
                consec+=1
            else:
                consec, pot_straight = 0, 0
            if consec >= 4:
                return ('SF', pot_straight)
        return ('F', flushhand)
    
    # Don't have a flush- check now for straights
    straighthand = []
    for card in hand:
        straighthand.append(card.val)
    if straighthand[0] == 14: straighthand.append(1)
    consec, pot_straight = 0,0
    for idx, val in enumerate(straighthand[:-1]):
        if val == straighthand[idx+1] + 1:
            if consec == 0:
                pot_straight = val
            consec+=1
        elif val == straighthand[idx+1]: continue
        else:
            consec, pot_straight = 0,0
        if consec >= 4:
            return ('S', pot_straight)
        
    # Don't have anything
    return ('N', 0)

def key_lookup(dict, search):
    for key, val in dict.items():
        if val == search:
            return key

class TwoWaySim:
    self.remove_set = set()

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        if player1.hole_cards_set:
            card1 = Card(self.player1.hole_cards[0][0], self.player1.hole_cards[0][1])
            card2 = Card(self.player1.hole_cards[1][0], self.player1.hole_cards[1][1])
            error_set_add((card1.rank, card1.suit))
            error_set_add((card2.rank, card2.suit))
        if player2.hole_cards_set:
            card1 = Card(self.player2.hole_cards[0][0], self.player2.hole_cards[0][1])
            card2 = Card(self.player2.hole_cards[1][0], self.player2.hole_cards[1][1])
            error_set_add((card1.rank, card1.suit))
            error_set_add((card2.rank, card2.suit))    
        self.pack = create_pack(self.remove_set)
        self.p1wins, self.p2wins, self.chops = 0, 0, 0

    def run_sim_simple(self, iterations):
        for i in range(iterations):
            gamepack = self.pack.copy()
            random.shuffle(gamepack)
            if not self.player1.hole_cards_set:
                self.player1.hole_cards.append(gamepack.pop())
                self.player1.hole_cards.append(gamepack.pop())
            if not self.player1.hole_cards_set:
                self.player1.hole_cards.append(gamepack.pop())
                self.player1.hole_cards.append(gamepack.pop())
        board = [gamepack.pop(), gamepack.pop(), gamepack.pop(), gamepack.pop(), gamepack.pop()]

    def error_set_add(self, card):
        if card in self.remove_set:
            print(f"ERROR: {str(card[0]) + str(card[1])} already taken")
            return 0
        else:
            self.remove_set.add(card)
