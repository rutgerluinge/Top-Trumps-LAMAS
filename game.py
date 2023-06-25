from typing import List, Tuple, Dict

import numpy as np
import random

import itertools
import networkx as nx
import matplotlib.pyplot as plt

from state import GameState
from strategies import RandomStrategy, HighStatStrategy, KnowledgeStrategy
from utils import loadCards
from cfg import GameConfig, CardConfig, GameMode
from cards import Card, init_cards, copy_card, EmptyCard, Deck
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
        self.next_round_starter = (
            "Player 0"  # gets to start first #just for logging this line
        )
        self.last_winner = None
        self.last_chosen_stat = -1
        self.scores = dict()

    # Initialize and start the game
    def start_game(self, config: GameConfig):
        self.initialize_game(config)
        self.game_loop()

    def initialize_game(self, config: GameConfig):
        card_list = init_cards(
            config.player_count, config.cards_pp, config.stats_count, config.stat_points
        )
        self.state.deck = card_list
        self.state.players = []
        self.config = config

        # Initialize players with cards from the cardList.
        for idx in range(self.config.player_count):
            name = f"Player {idx}"

            # create "smart" player
            if idx == 0:
                player = Player(
                    name=name,
                    idx=idx,
                    card_list=card_list[
                        idx * config.cards_pp : (idx + 1) * config.cards_pp
                    ],
                    config=config,
                    strategy=KnowledgeStrategy(),
                )
            # create other players TODO can also do if else, if we want multiple smart agents/testing:
            else:
                player = Player(
                    name=name,
                    idx=idx,
                    card_list=card_list[
                        idx * config.cards_pp : (idx + 1) * config.cards_pp
                    ],
                    config=config,
                    strategy=RandomStrategy(),
                )

            self.state.players.append(player)
            self.scores[player] = 0

    def game_loop(self):
        while not self.has_ended():
            if self.config.generate_kripke:
                self.createKripkeModel()
            playedCards, winner, stat_idx = self.play_round()
            if self.update_game_state(playedCards, winner, stat_idx):
                break

    def start_player(self, start_player_idx=0):
        """method which return player idx which should start next round, if no winner yet (first round) player 0
        starts"""
        if self.last_winner is None:
            return self.state.players[start_player_idx]
        return self.last_winner

    def play_round(self):
        # The next player takes a turn.
        start_player: Player = self.start_player()

        stat_idx = start_player.start_turn()
        self.last_chosen_stat = stat_idx  # for mesa for now

        winner: Player
        round_result = {}
        for player in self.state.players:
            if player.get_name() in self.eliminated_players:
                continue
            round_result[player] = player.match_stat(stat_idx=stat_idx)

        # sorted list of stat values in play
        round_result = dict(
            sorted(round_result.items(), key=lambda x: x[1], reverse=True)
        )  # todo change this for ties!
        winner = next(iter(round_result))
        self.next_round_starter = winner.name

        # collect the cards that were played in this round
        card_pool = self.collect_cards()

        return card_pool, winner, stat_idx

    def collect_cards(self) -> dict:
        """collects all the cards that were played in the active round"""
        card_pool = dict()
        # get all cards from each player
        for player in self.state.players:
            if player.get_name() in self.eliminated_players:
                continue
            # in the epistemic game mode, all cards remain with the players
            if self.config.game_mode == GameMode.STANDARD:
                card_pool[player.idx] = player.hand_card()
            else:
                card_pool[player.idx] = player.get_top_card()

        return card_pool

    def update_game_state(
        self, card_pool: Dict[int, Card], winner: Player, stat_idx: int
    ) -> bool:
        """Updates the game state. Returns true if there is a winner, false otherwise"""
        # Add all won cards to the list of the winner.
        if self.config.game_mode == GameMode.STANDARD:
            # updates and shuffles the cards for the winner
            winner.give_cards(cards=list(card_pool.values()))
        else:
            # all cards should be shuffled but none are transferred
            for player in self.players_in_game():
                player.shuffle_cards()

        self.update_player_beliefs(card_pool, winner, stat_idx)

        if self.config.debug:
            self.print()

        for key, value in self.eliminated_players.items():
            if value == self.round:
                print(f"player: {key}, got eliminated in round {value}")

        players = self.players_in_game()
        # update the score
        self.scores[winner] += 1
        self.last_winner = winner
        # check if we have a winner
        if self.has_winner():
            print("Game is over, ", players[0].get_name(), " won the game!")
            return True
        self.round += 1

        return False

    def update_player_beliefs(
        self, card_pool: Dict[int, Card], winner: Player, stat_idx: int
    ):
        # update players individual beliefs
        if self.config.full_announcement:
            # all players know all whole cards
            for player in self.state.players:
                knowledge = winner_knowledge(card_pool)
                player.update_beliefs(cards=knowledge, winner_idx=winner.idx)
        else:
            # only winner knows all whole cards, losers know relevant stat
            for player in self.state.players:
                if player == winner:
                    knowledge = winner_knowledge(card_pool)  # winner knows whole cards
                else:
                    knowledge = loser_knowledge(
                        card_pool, stat_idx=stat_idx
                    )  # losers only know relevant stat + name is now to in winner his hands

                player.update_beliefs(cards=knowledge, winner_idx=winner.idx)

    def players_in_game(self) -> list[Player]:
        """:returns players that are still playing (and only 1 if there is a winner)"""
        still_playing = []
        for player in self.state.players:
            if player.has_cards():
                still_playing.append(player)
            elif player.get_name() not in self.eliminated_players.keys():
                self.eliminated_players[player.get_name()] = self.round

        return still_playing

    def has_winner(self) -> bool:
        # a standard game has a winner if there is only one player left
        if self.config.game_mode == GameMode.STANDARD:
            return len(self.players_in_game()) == 1
        elif self.is_at_round_or_point_limit():
            return self.single_high_scorer()

        return False

    def game_winner(self) -> Player:
        """Returns the game winner, if there is one"""
        if not self.has_winner():
            return None
        if self.config.game_mode == GameMode.STANDARD:
            return self.players_in_game()[0]
        elif (
            self.config.game_mode == GameMode.EPISTEMIC_ROUND_LIMIT
            or self.config.game_mode == GameMode.EPISTEMIC_POINT_LIMIT
        ):
            return self.single_high_scorer()
        return None

    def is_at_round_or_point_limit(self) -> bool:
        """Returns true if the game has ended by reaching the maximum number of rounds or points"""
        if self.config.game_mode == GameMode.EPISTEMIC_ROUND_LIMIT:
            return self.round >= self.config.max_round_or_score
        elif self.config.game_mode == GameMode.EPISTEMIC_POINT_LIMIT:
            high_scorer = self.single_high_scorer()
            return (
                high_scorer != None
                and self.scores[high_scorer] >= self.config.max_round_or_score
            )

        return False

    def has_ended(self) -> bool:
        if self.has_winner():
            return True

        if self.config.game_mode == GameMode.EPISTEMIC_ROUND_LIMIT:
            return self.is_at_round_or_point_limit()

    def single_high_scorer(self) -> Player:
        """returns the player with the single highest score, if any"""
        high_score = max(self.scores.values())
        if list(self.scores.values()).count(high_score) == 1:
            return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)[0][0]
        return None

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
        state = f"Game: Round {self.round}\n" + str(self.state)
        return state

    def createKripkeModel(self):
        # Create instance of graph
        graph = nx.Graph()

        cards = []
        for player in self.state.players:
            for card in player.cardList:
                cards.append(card.name[:2])

        worlds = []

        allCombis = []
        for player in self.state.players:
            combis = []
            for i in range(len(cards) + 1):
                for combi in itertools.combinations(cards, i):
                    if len(combi) == len(player.cardList):
                        combis.append(combi)
            allCombis.append(combis)

        # For 2 players
        possibleCombis = []
        if len(self.state.players) == 2:
            for combi in allCombis[0]:
                for combi2 in allCombis[1]:
                    dupes = [i for i in combi if i in combi2]
                    if len(dupes) == 0:
                        possibleCombis.append([combi, combi2])

        # For 3 players
        if len(self.state.players) == 3:
            for combi in allCombis[0]:
                for combi2 in allCombis[1]:
                    dupes = [i for i in combi if i in combi2]
                    if len(dupes) == 0:
                        for combi3 in allCombis[2]:
                            dupes = [i for i in combi3 if i in combi + combi2]
                            if len(dupes) == 0:
                                possibleCombis.append([combi, combi2, combi3])

        for combi in possibleCombis:
            world = ""
            for player in combi:
                world += "{"
                for name in player:
                    world += name + ","
                if world.endswith(","):
                    world = world[:-1]
                world += "}, "
            world = world[:-2]
            worlds.append(world)

        worlds = self.checkBeliefs(worlds)

        # Create edges for every world connecting with every other world
        edges = []
        for i in range(len(worlds)):
            for j in range(i, len(worlds)):
                edges.append((worlds[i], worlds[j]))

        # Create graph and store it in self
        graph.add_nodes_from(worlds)
        graph.add_edges_from(edges)
        self.state.kripkeModel = graph

        self.showKripkeModel()

    def showKripkeModel(self):
        # Drawing options
        options = {
            "node_size": 400,
            "with_labels": True,
            # "font_weight": 'bold',
            "width": 1,
        }

        nx.draw_circular(self.state.kripkeModel, **options)
        print("show_plot")
        plt.show()

    # Function to check which possible worlds are no longer possible due to an agents belief
    def checkBeliefs(self, worlds):
        new_worlds = worlds.copy()

        # Check for every world wether it has to be removed
        for world in worlds:
            # Get the belief of only one player (Every player has the same belief)
            for belief in self.state.players[0].agent_knowledge.belief.keys():
                world_things = world.split("{")
                if world_things[0] == "":
                    del world_things[0]

                # Check every card in the agent's belief per player and check whether
                # the world contains those cards for that player, if not, the world
                # can be removed.
                for card in self.state.players[0].agent_knowledge.belief[belief]:
                    equals = False
                    for thing in world_things[belief].split("}")[0].split(","):
                        if thing == card.name[:2]:
                            equals = True
                    if not equals:
                        if world in new_worlds:
                            new_worlds.remove(world)

        return new_worlds
