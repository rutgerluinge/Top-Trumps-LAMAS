

# Player class to create an instance for each player participating in the game.
class Player:
    def __init__(self, name, cardList):
        self.name = name
        self.cardList = cardList

    # Debug print function for players
    def print(self):
        print("Name", self.name)
        for card in self.cardList:
            card.print()

# Card class to create an instance of each available card.
class Card:
    def __init__(self, name, stat1, stat2):
        self.name = name
        self.stat1 = stat1
        self.stat2 = stat2

    # Debug function to print card stats.
    def print(self):
        print("  Name", self.name)
        print("    Friendship", self.stat1)
        print("    Intelligence", self.stat2)