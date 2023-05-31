import numpy as np
import random

from utils import loadCards
from cfg import GameConfig
from classes import Player, Card


# Main class to track the game
class Game:
    def __init__(self):
        self.playerList = []
        self.config = GameConfig()

    # Initialize and start the game
    def startGame(self, config: GameConfig):
        loaded_card_count, cardList = loadCards()
        self.config = config

        if loaded_card_count > self.config.card_count:
            loaded_card_count = self.config.card_count

        # Initialize players with cards from the cardList.
        for i in range(self.config.player_count):
            self.playerList.append(
                Player(
                    "Player " + str(i),
                    cardList[
                        i
                        * int(loaded_card_count / self.config.player_count) : (i + 1)
                        * int(loaded_card_count / self.config.player_count)
                    ],
                )
            )

        self.gameLoop()

    def gameLoop(self):
        self.print()
        playerIdx = -1
        while True:
            # The next player takes a turn.
            playerIdx = (playerIdx + 1) % len(self.playerList)
            player = self.playerList[playerIdx]

            # Card to play from current player
            activeCard = player.cardList[0]
            player.cardList = player.cardList[1:]

            # Choose which stat to play
            stat = player.makeDecision(activeCard)

            # Gather all the cards to check the stats of
            playedCards = [activeCard]
            for otherPlayer in self.playerList:
                if otherPlayer == player:
                    continue
                playedCards.append(otherPlayer.cardList[0])
                otherPlayer.cardList = otherPlayer.cardList[1:]

            # Print played cards if debug mode is on.
            if self.config.debug:
                print("Played Cards:")
                for card in playedCards:
                    card.print()
                print("Chosen stat:", stat)

            # Find who won the round.
            winner = -1
            best = 0
            for i, card in enumerate(playedCards):
                if card.stats[stat] > best:
                    best = card.stats[stat]
                    winner = i

            if self.config.debug:
                print("The winner is: Player", winner)

            if self.updateGameState(playedCards, winner):
                break

    def updateGameState(self, playedCards, winner):
        # Add all won cards to the list of the winner.
        self.playerList[winner].cardList = np.concatenate(
            (self.playerList[winner].cardList, playedCards)
        )

        # Reshuffle the cards from the winner.
        random.shuffle(self.playerList[winner].cardList)

        if self.config.debug:
            self.print()

        # Check if any players are elimated.
        for i in range(len(self.playerList)):
            if len(self.playerList[i].cardList) == 0:
                print("Game over for: Player", i)
                del self.playerList[i]
                i -= 1

        # Check if game is won.
        if len(self.playerList) == 1:
            print("Game is over, ", self.playerList[0].name, "won the game!")
            return True

        return False

    # Debug function to print the game status.
    def print(self):
        print("Game:")
        for player in self.playerList:
            player.print()
