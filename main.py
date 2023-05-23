import numpy as np
import json

# Global parameter. TODO: set adjustable on front end.
CARD_COUNT = -1 # This is set properly upon loading of cards
PLAYER_COUNT = 2

def loadCards():
    # Initialize empty card list.
    cardList = []

    # Load card data from json file.
    data = json.load(open('cards.json'))

    # Create a card for each entry and add it to the card list.
    for name in data:
        card = Card(data[name]['name'], data[name]['stat1'], data[name]['stat2'])
        cardList.append(card)

    # Update global parameter for the number of cards used in the game.
    CARD_COUNT = len(cardList)

    # Return the list of loaded cards.
    return cardList

# Controls the main loop of the game
def gameLoop():
    x = 0

# Initializes all aspects of the game
def initGame():
    cardList = loadCards()

    for card in cardList:
        card.print()

# Main function obviously
def main():
    initGame()

if __name__=='__main__':
    main()