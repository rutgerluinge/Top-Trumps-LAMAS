from typing import List, Dict

import numpy as np

from agent_state import AgentKnowledge
from cards import Card, Deck, EmptyCard
from abc import ABC, abstractmethod

from cfg import GameConfig
from strategies import Strategy


class Player:
    def __init__(
        self,
        name: str,
        idx: int,
        card_list: Deck,
        config: GameConfig,
        strategy: Strategy,
    ):
        self.name = name
        self.idx = idx
        self.cardList = card_list
        self.config = config
        self.strategy = strategy
        self.agent_knowledge = AgentKnowledge(self.config, player_idx=idx)

    # Function to decide which stat to use based on the current card
    # Currently just returns a random one.
    def get_top_card(self) -> Card:
        """get instance of the top card,
        @:returns Card"""
        if len(self.cardList) == 0:
            return None
        return self.cardList[0]

    def match_stat(self, stat_idx: int) -> int:
        """:returns stat value of given stat idx of top card"""
        card = self.get_top_card()
        return card.stats[stat_idx]

    def start_turn(self) -> int:
        """:returns stat idx TODO now it is random change later with strategy"""

        return self.strategy.choose_action(
            top_card=self.get_top_card(), state=self.agent_knowledge
        )

    # adds the given ca
    def give_cards(self, cards: List[Card]):
        """:param won cards, method adds cards and shuffles them"""
        for card in cards:
            self.cardList.append(card)
        self.shuffle_cards()

    def shuffle_cards(self):
        """shuffles this player's deck"""
        np.random.shuffle(self.cardList)

    def update_beliefs(self, cards: Dict[int, EmptyCard], winner_idx: int):
        self.agent_knowledge.update_belief(cards, winner_idx=winner_idx)

        if self.idx == 0 and self.config.debug:
            self.agent_knowledge.debug()

    def update_beliefs_dumb(self):
        raise NotImplementedError

    # Debug print function for players
    def __str__(self) -> str:
        state = self.name
        for card in self.cardList:
            state += "\n\t" + str(card)
        return state

    def has_cards(self) -> bool:
        """:returns bool to see if player is still in the game (instead of removing player)"""
        return len(self.cardList) > 0

    def hand_card(self) -> Card:
        """:returns card and removes from top deck"""
        return self.cardList.pop(0)

    def get_name(self) -> str:
        return self.name

    def get_deck(self) -> Deck:
        return self.cardList
