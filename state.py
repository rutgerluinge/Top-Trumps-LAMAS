import agents
import cards

PlayerList = list[agents.AbstractAgent]


# Representation of the game state. Entire true state can be modeled by this class and evaluated/observed in a few different ways
# Indirectly tracks where cards are through the fact that players track the cards in their pile
class GameState:
    players: PlayerList = []
    deck: cards.Deck = []

    # Initialize the game state. Players and deck may be known but cards are not dealt
    def __init__(self, players: PlayerList = [], deck: cards.Deck = []):
        self.players = players
        self.deck = deck

    # Returns the game state as a dictionary of cards and players
    # Can be used to iterate the deck and find which player it belongs to
    def as_dictionary(self) -> dict():
        stateDictionary = dict()
        for player in self.players:
            for card in player.get_deck():
                stateDictionary[card] = player
        return stateDictionary

    # Returns the game state as an array of integers, as described in the formal description section in the report
    # Each index in the array represents the index of a card in the game deck, and the number of the array refers to the index of the player that currently owns that card
    def as_integer_array(self) -> list[int]:
        array = []
        dictionary = self.as_dictionary()
        # iterate over the cards and get the index of the card in the playerlist
        for card in self.deck:
            array.append(self.players.index(dictionary[card]))
        return array

    # Returns the ordered concatenated string of players
    def __str__(self) -> str:
        string = str()
        for player in self.players:
            string += "\t" + str(player)
            if (player != self.players[-1]):
                string += "\n"
        return string
