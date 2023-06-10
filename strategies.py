from abc import ABC, abstractmethod

from cards import Card


class Strategy(ABC):

    @abstractmethod
    def choose_action(self, top_card:Card):
        pass