from typing import List, Tuple, Dict

import numpy as np
import random

from state import GameState
from strategies import RandomStrategy, HighStatStrategy, KnowledgeStrategy
from utils import loadCards
from cfg import GameConfig, CardConfig
from cards import Card, init_cards, copy_card, EmptyCard
from agents import Player


def winner_knowledge(cards: Dict[int, Card]):
    knowledge = dict()
    for key, card in cards.items():
        knowledge[key] = copy_card(card)
    return knowledge


def loser_knowledge(cards: Dict[int, Card], stat_idx: int):
    knowledge = dict()
    for key, real_card in cards.items():
        card = EmptyCard(name=real_card.name)
        card.update_card_stat(stat_idx, real_card.stats[stat_idx])

        knowledge[key] = card
    return knowledge


# Main class to track the game
class Game:
    def __init__(self):
        self.state = GameState()
        self.config = GameConfig()
        self.eliminated_players = dict()
        self.round = 1
        self.next_round_starter = "Player 0"  # gets to start first #just for logging this line
        self.last_winner = None
        self.last_chosen_stat = -1

    # Initialize and start the game
    def startGame(self, config: GameConfig):
        self.initializeGame(config)
        self.gameLoop()

    def initializeGame(self, config: GameConfig):
        card_list = init_cards(config.player_count, config.cards_pp, config.stats_count, config.stat_points)
        self.state.deck = card_list
        self.state.players = []
        self.config = config

        # Initialize players with cards from the cardList.
        for idx in range(self.config.player_count):
            name = f"Player {idx}"

            # create "smart" player
            if idx == 0:
                player = Player(name=name,
                                idx=idx,
                                card_list=card_list[idx * config.cards_pp: (idx + 1) * config.cards_pp],
                                config=GameConfig(),
                                strategy=KnowledgeStrategy())
            # create other players TODO can also do if else, if we want multiple smart agents/testing:
            else:
                player = Player(name=name,
                                idx=idx,
                                card_list=card_list[idx * config.cards_pp: (idx + 1) * config.cards_pp],
                                config=GameConfig(),
                                strategy=RandomStrategy())

            self.state.players.append(player)

    def gameLoop(self):
        while True:
            playedCards, winner, stat_idx = self.playRound()
            if self.updateGameState(playedCards, winner, stat_idx):
                break

    def start_player(self, start_player_idx=0):
        """method which return player idx which should start next round, if no winner yet (first round) player 0
        starts """
        if self.last_winner is None:
            return self.state.players[start_player_idx]
        return self.last_winner

    def playRound(self):
        # The next player takes a turn.
        start_player: Player = self.start_player()

        stat_idx = start_player.start_turn()
        self.last_chosen_stat = stat_idx  # for mesa for now

        round_result = {}
        for player in self.state.players:
            if player.get_name() in self.eliminated_players:
                continue
            round_result[player.get_name()] = player.match_stat(stat_idx=stat_idx)

        round_result = dict(
            sorted(round_result.items(), key=lambda x: x[1], reverse=True))  # todo change this for ties!
        winner_name = next(iter(round_result))
        self.next_round_starter = winner_name

        card_pool = dict()
        winner: Player

        """Get all cards, and 'remember' winner"""
        for player in self.state.players:
            if player.get_name() == winner_name:
                winner = player
            if player.get_name() in self.eliminated_players:
                continue
            card_pool[player.idx] = player.hand_card()

        return card_pool, winner, stat_idx

    def updateGameState(self, card_pool: Dict[int, Card], winner: Player, stat_idx: int):
        # Add all won cards to the list of the winner.
        winner.give_cards(cards=list(card_pool.values()))  # updates and shuffles

        #update players individual beliefs
        if self.config.full_announcement:
            # all players know all whole cards
            for player in self.state.players:
                knowledge = winner_knowledge(card_pool)
                player.update_beliefs(cards=knowledge, winner_idx=winner.idx)
        else: 
            # only winner knows all whole cards, losers know relevant stat
            for player in self.state.players:
                if player == winner:
                    knowledge = winner_knowledge(card_pool) #winner knows whole cards
                else:
                    knowledge = loser_knowledge(card_pool, stat_idx=stat_idx)       #losers only know relevant stat + name is now to in winner his hands

                player.update_beliefs(cards=knowledge, winner_idx=winner.idx)



        if self.config.debug:
            self.print()

        winner, players = self.players_in_game()

        for key, value in self.eliminated_players.items():
            if value == self.round:
                print(f"player: {key}, got eliminated in round {value}")

        # check if we have a winner
        if winner:
            print("Game is over, ", players[0].get_name(), " won the game!")
            return True
        self.round += 1

        return False

    def players_in_game(self) -> tuple[bool, list[Player]]:
        """:returns players that are still playing (and only 1 if there is a winner) + boolean if winner is found"""
        still_playing = []
        for player in self.state.players:
            if player.has_cards():
                still_playing.append(player)
            elif player.get_name() not in self.eliminated_players.keys():
                self.eliminated_players[player.get_name()] = self.round

        if len(still_playing) == 1:  # winner known:
            return True, still_playing

        return False, still_playing

    # Debug function to print the game status.
    def print(self):
        print(str(self))

    def print_interface(self):
        """print mesa interface (bit prettier for now)"""
        state = ""
        state += f"Player which may choose next round: {self.next_round_starter} \n"
        state += f"Round {self.round} \n"

        state += f"\t  chosen stat: {CardConfig.stat_names[self.last_chosen_stat]}"
        for player in self.state.players:
            state += "\n\t" + str(player)
        return state

    def __str__(self) -> str:
        state = "Game: \n" + str(self.state)
        return state
