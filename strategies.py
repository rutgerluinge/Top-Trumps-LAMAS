from abc import ABC, abstractmethod

from cards import Card
# from state import GameState
import numpy as np

class Strategy(ABC):

    @abstractmethod
    def choose_action(self, top_card:Card, state):    #gamestate should maybe be replaced with playerstate?
        pass



class RandomStrategy(Strategy):
    """chooses random stat of the card"""
    def choose_action(self, top_card: Card, state):
        return np.random.randint(0, len(top_card.stats))


class HighStatStrategy(Strategy):
    """Chooses highest stat of the card"""
    def choose_action(self, top_card: Card, state):
        return np.argmax(top_card.stats)


class KnowledgeStrategy(Strategy):
    """Some sort of smart propability distribution"""
    def choose_action(self, top_card: Card, state):
        raise NotImplementedError