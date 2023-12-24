import random
from collections import defaultdict
from card import Card
from deck import create_pack
from player import Player
from cardmappings import mappings

class TwoWaySim:
    """
    Class handling simulation of poker hand between 2 players.
    Board specification is optional.
    """
    def __init__(self, player1, player2, spec_board = []):
        """
        Initializes 2 way simulation.
        """
        self.remove_set = set()
        self.spec_board = spec_board.copy()
        self.player1 = player1
        self.player2 = player2

        self.create_game_pack()

        self.p1wins, self.p2wins, self.chops = 0, 0, 0
        self.conditional = 0

    def run_sim_simple(self, iterations, report = False):
        for i in range(iterations):
            self.player1.reset()
            self.player2.reset()
            gamepack = self.pack.copy()
            random.shuffle(gamepack)
            if not self.player1.hole_cards_set:
                self.player1.hole_cards.append(gamepack.pop())
                self.player1.hole_cards.append(gamepack.pop())
            if not self.player2.hole_cards_set:
                self.player2.hole_cards.append(gamepack.pop())
                self.player2.hole_cards.append(gamepack.pop())
            board = []
            for card in self.spec_board: board.append(card)
            for i in range(5-len(self.spec_board)):
                board.append(gamepack.pop())
            p1hand = board.copy() + self.player1.hole_cards.copy()
            p2hand = board.copy() + self.player2.hole_cards.copy()
            self.player1.add_hand(p1hand)
            self.player2.add_hand(p2hand)
            res = self.player1.hand_compare(self.player2)
            if res < 0: self.p2wins+=1
            elif res == 0: self.chops+=1
            else: self.p1wins+=1
        if report:
            print(f"{self.player1.name} win percent: {(self.p1wins/iterations)*100:.2f}%")
            print(f"{self.player2.name} win percent: {(self.p2wins/iterations)*100:.2f}%")
            print(f"Chop percent: {(self.chops/iterations)*100:.2f}%")

    def run_sim_condition(self, iterations, report = False):
        for i in range(iterations):
            self.player1.reset()
            self.player2.reset()
            gamepack = self.pack.copy()
            random.shuffle(gamepack)
            if not self.player1.hole_cards_set:
                self.player1.hole_cards.append(gamepack.pop())
                self.player1.hole_cards.append(gamepack.pop())
            if not self.player2.hole_cards_set:
                self.player2.hole_cards.append(gamepack.pop())
                self.player2.hole_cards.append(gamepack.pop())
            board = []
            for card in self.spec_board: board.append(card)
            for i in range(5-len(self.spec_board)):
                board.append(gamepack.pop())
            p1hand = board.copy() + self.player1.hole_cards.copy()
            p2hand = board.copy() + self.player2.hole_cards.copy()
            self.player1.add_hand(p1hand)
            self.player2.add_hand(p2hand)
            res = self.player1.hand_compare(self.player2)

            if self.player2.hole_cards[0].rank == 'A' and \
                self.player2.hole_cards[1].rank == 'A' and \
                self.player1.hole_cards[0].rank == 'A' and \
                self.player1.hole_cards[1].rank == 'A':
                self.conditional+=1
                if self.player1.handstrength[0] == "Flush" and \
                self.player2.handstrength[1] != "Flush":
                    self.conditional+=1
                elif self.player1.handstrength[0] != "Flush" and \
                self.player2.handstrength[1] == "Flush":
                    self.conditional+=1
                
        if report:
            number = (self.conditional/iterations) * 100
            formatted_number = '{:.8f}'.format(number).rstrip('0').rstrip('.')
            print(f'{formatted_number}% chance of occuring')

    def create_game_pack(self):
        """
        Method for creating a custom game pack that accounts for removing
        cards held by players.
        """
        if self.player1.hole_cards_set:
            for i in range(2):
                self.error_set_add(self.player1.hole_cards[i])
        if self.player2.hole_cards_set:
            for i in range(2):
                self.error_set_add(self.player2.hole_cards[i])
        if len(self.spec_board) != 0:
            for card in self.spec_board: self.error_set_add(card)
        
        self.pack = create_pack(self.remove_set)
        



    def error_set_add(self, card):
        if card in self.remove_set:
            print(f"ERROR: {card} already taken")
            exit(1)
        else:
            self.remove_set.add(card)
