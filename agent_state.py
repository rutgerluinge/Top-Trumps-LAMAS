from typing import List, Dict, Tuple

from cards import EmptyCard, Card, copy_card, concatenate_cards
from cfg import GameConfig


class AgentKnowledge:
    def __init__(self, config: GameConfig, player_idx):
        self.config: GameConfig = config
        self.player_idx = player_idx
        self.belief: Dict[int, List[EmptyCard]] = dict()
        self.player_cards: Dict[int, int] = dict()
        # init start state
        self.reset_knowledge()

    def reset_knowledge(self):
        for player in range(self.config.player_count):
            self.belief[player] = []
            self.player_cards[player] = self.config.cards_pp

    def update_cards(self, cards: Dict[int, EmptyCard], winner_idx: int):
        """dictionary is necessary as we have to make sure the player and card are matched"""

        for idx_player, card in cards.items():

            self.player_cards[idx_player] -= 1  # correct card count
            self.player_cards[winner_idx] += 1  # correct card count

            old_known_card = self.remove_card_by_name(card.name,
                                                      idx_player)  # remove cards of losing players: belief of player
            self.match_cards(winner_idx, old_known_card, card)

    def match_cards(self, winner_idx, old_card, new_card):
        self.belief[winner_idx].append(concatenate_cards(old_card, new_card))

        # give cards to winner

    def debug(self):
        print(f"card counts: ")
        for player, card_cnt in self.player_cards.items():
            print(f"player {player} cards: {card_cnt}")

        for player_idx, cards in self.belief.items():
            print(f"player {player_idx}")
            for card in cards:
                print(f"\t  name: {card.name}, stats: {card.stats}")
            print()

    def __str__(self):
        print(f"player {self.player_idx} has belief:")
        for idx, key in enumerate(self.belief.keys()):
            print(f"    {idx} = {self.belief[key]}")

    def remove_card_by_name(self, name: str, player_idx: int):
        """check if you can do this! with if known_by_player"""
        for idx, card in enumerate(self.belief[player_idx]):
            if card.name == name:
                return self.belief[player_idx].pop(idx)  # removes card from knowledge
        return None

    def known_by_player(self, card_name, player_idx) -> bool:
        """:returns true if this agent knew, that the other agent had a card with NAME (and can thus remove it later)"""
        for card in self.belief[player_idx]:
            if card.name == card_name:
                return True
        return False

    def find_card_by_name(self, name, object_list: List[Card]) -> Tuple[bool, EmptyCard]:
        """:returns bool: known card? and the new knowledge card"""
        for card in object_list:
            if card.name == name:
                return True, copy_card(card)

        return False, EmptyCard(name=None, stat_count=self.config.stats_count)
