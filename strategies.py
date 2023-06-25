from abc import ABC, abstractmethod
from typing import List

from agent_state import AgentKnowledge
from cards import Card, EmptyCard

# from state import GameState   #todo this causes circular import :/
import numpy as np

from cfg import GameConfig


class Strategy(ABC):
    @abstractmethod
    def choose_action(
        self, top_card: Card, state
    ):  # gamestate should maybe be replaced with playerstate?
        pass


class RandomStrategy(Strategy):
    """chooses random stat of the card"""

    def choose_action(self, top_card: Card, state: AgentKnowledge):
        return np.random.randint(0, len(top_card.stats))


class HighStatStrategy(Strategy):
    """Chooses highest stat of the card"""

    def choose_action(self, top_card: Card, state: AgentKnowledge):
        return np.argmax(top_card.stats)


def pair_wise_comparison(stats: List[int], other_stats: List[int]):
    result = [0] * len(stats)
    idx = 0
    for stat1, stat2 in zip(stats, other_stats):
        if stat2 is None:
            idx += 1
            continue

        if stat1 >= stat2:  # equal because draw is also win
            result[idx] = 1

        idx += 1
    return result


class KnowledgeStrategy(Strategy):
    """CHoose stat with most pairwise wins (propability)"""

    def choose_action(self, top_card: Card, state: AgentKnowledge):
        odds = [0] * GameConfig.stats_count

        for player_idx in state.belief.keys():
            if player_idx == state.player_idx:
                continue  # do not use chance against yourself, net necessary

            known_cards: List[EmptyCard] = state.belief[player_idx]
            for card in known_cards:
                win = pair_wise_comparison(top_card.stats, card.stats)
                odds = np.add(odds, win)
        print(
            f"player chooses stat {np.argmax(odds)} with card stats {top_card.stats} as a result of smart strategy"
        )
        return np.argmax(odds)
