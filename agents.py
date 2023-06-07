from typing import List

import numpy as np

from cards import Card, Deck
from abc import ABC, abstractmethod

from cfg import GameConfig


class AbstractAgent(ABC):
    """abstract class"""

    def get_top_card(self):
        pass
    @abstractmethod
    def match_stat(self, stat_idx:int) -> int:
        pass

    @abstractmethod
    def start_turn(self):
        pass

    @abstractmethod
    def has_cards(self) -> bool:
        pass
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_deck(self) -> Deck:
        pass

    def hand_card(self):
        pass

    def give_cards(self, cards: Deck):
        pass

    def __str__(self) -> str:
        pass



class Player(AbstractAgent):
    def __init__(self, name: str, card_list: Deck, config: GameConfig):
        self.name = name
        self.cardList = card_list
        self.config = config

    # Function to decide which stat to use based on the current card
    # Currently just returns a random one.
    def get_top_card(self) -> Card:
        """get instance of the top card,
        @:returns Card"""
        if len(self.cardList) == 0:
            return None
        return self.cardList[0]

    def match_stat(self, stat_idx:int) -> int:
        """:returns stat value of given stat idx of top card"""
        card = self.get_top_card()
        return card.stats[stat_idx]

    def start_turn(self) -> int:
        """:returns stat idx TODO now it is random change later with strategy"""
        return np.random.randint(0, self.config.stats_count)

    def give_cards(self, cards: List[Card]):
        """:param won cards, method adds cards and shuffles them"""
        for card in cards:
            self.cardList.append(card)
        np.random.shuffle(self.cardList)

    # Debug print function for players
    def __str__(self) -> str:
        state = self.name
        for card in self.cardList:
            state += "\t\n" + str(card)
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

class DumbAgent(AbstractAgent):
    def make_decision(self, card: Card):
        pass

    def start_turn(self):
        pass
