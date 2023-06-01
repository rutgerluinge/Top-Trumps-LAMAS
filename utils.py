import json
import random

from cards import Card
import cfg

def loadCards():
    # Initialize empty card list.
    cardList = []

    # Load card data from json file.
    data = json.load(open('cards.json'))

    # Create a card for each entry and add it to the card list.
    for name in data:
        statList = []
        for i in range(cfg.STATS_COUNT):
            statList.append(data[name]['stat' + str(i + 1)])
        card = Card(data[name]['name'], statList)
        cardList.append(card)

    # Shuffle the deck of cards
    random.shuffle(cardList)

    # Return the list of loaded cards.
    return len(cardList), cardList