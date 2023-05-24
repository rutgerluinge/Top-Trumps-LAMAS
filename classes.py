import random
import numpy as np

# Player class to create an instance for each player participating in the game.
class Player:
    def __init__(self, name, cardList):
        self.name = name
        self.cardList = np.array(cardList)

    # Function to decide which stat to use based on the current card
    # Currently just returns a random one.
    def makeDecision(self, card):
        return random.randint(0, len(card.stats) - 1)

    # Debug print function for players
    def print(self):
        print(self.name)
        for card in self.cardList:
            card.print()

# Card class to create an instance of each available card.
class Card:
    def __init__(self, name, stats):
        self.name = name
        self.stats = np.array(stats)

    # Debug function to print card stats.
    def print(self):
        print("  Card:", self.name)
        for i, stat in enumerate(self.stats):
            print("    stat" + str(i) + ":", stat)