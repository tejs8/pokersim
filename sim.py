from itertools import product, combinations
import matplotlib.pyplot as plt
from headsup import *
from player import Player

# Dan = Player(name = "Dan", holecards = [[10, 'S'], [10, 'D']])
# Tej = Player(name = "Tej")
# game = TwoWaySim(Dan, Tej)
# game.run_sim_simple(10000, True)

"""
def generate_hands():
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    suits = ['H', 'S', 'C', 'D']
    deck = [[rank, suit] for rank, suit in product(ranks, suits)]
    hands = list(combinations(deck, 2))
    return hands

h = generate_hands()
for ha in h:
    print(h)
    print()
exit(0)
"""

res = []
for i in range(50):
    Dan = Player(name = "Dan", holecards = [[3, 'H'], [4, 'D']])
    Tej = Player(name = "Tej", holecards=[[6,'S'], [3,'S']])
    game = TwoWaySim(Dan, Tej, [Card(9, 'C'), Card('K', 'H'), Card(5, 'S'), Card(2,'S')])
    game.run_sim_simple(10000, True)
    res.append([i, 13.64-(game.p1wins/10000)])

x,y = zip(*res)
plt.plot(x,y,'o-')
plt.ylim([12, 15])
plt.savefig('/root/Desktop/poker/my_plot.png') 