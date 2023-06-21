from typing import List

import numpy as np
from cfg import GameConfig, CardConfig


class Card:
    stat_names = CardConfig.stat_names

    def __init__(self, name, stats):
        self.name = name
        self.stats = np.array(stats)

    def __str__(self) -> str:
        state = "  Card: " + self.name
        for i, stat in enumerate(self.stats):
            state += f" {CardConfig.stat_names[i]} = {stat},"

        return state


class EmptyCard:
    """TODO maybe not a good name as it is more like a memory buffer"""

    stat_names = CardConfig.stat_names

    def __init__(self, name, stat_count=GameConfig.stats_count):
        self.name = name
        self.stat_count = stat_count
        self.stats = [None for _ in range(self.stat_count)]

    def update_card_stat(self, idx: int, value: int):
        if idx > (self.stat_count - 1):
            raise "update card method has wrong input idx"
        self.stats[idx] = value

    def update_card_whole(self, card: Card):
        self.name = card.name
        self.stats = card.stats


def concatenate_cards(old_card: EmptyCard, new_card: EmptyCard):
    if old_card is None:
        return new_card

    if old_card.name != new_card.name:
        raise "error not equal card names"

    concat_card = EmptyCard(new_card.name)
    for idx in range(GameConfig.stats_count):
        if isinstance(old_card.stats[idx], np.int32):
            concat_card.update_card_stat(idx, old_card.stats[idx])
        elif isinstance(new_card.stats[idx], np.int32):
            concat_card.update_card_stat(idx, new_card.stats[idx])

    return concat_card


def copy_card(card: Card) -> EmptyCard:
    copy = EmptyCard(name=card.name, stat_count=len(card.stats))
    copy.update_card_whole(card=card)
    return copy


# Type alias
Deck = list[Card]


def random_stats(total_stats: int, stat_points: int):
    """method to randomly create stats (evenly)"""
    stats = [0 for _ in range(total_stats)]

    current_points = sum(stats)
    while current_points != stat_points:
        index = np.random.randint(0, total_stats)
        # Calculate the difference between the current value and the desired sum
        diff = stat_points - current_points
        # Generate a random value within the difference range
        if diff == 1:
            random_value = 1
        else:
            random_value = np.random.randint(1, diff)
        # Update the array with the new random value
        stats[index] += random_value
        # Update the current sum
        current_points = sum(stats)
    return stats


def init_cards(
    player_count=2, cards_per_player=2, stats_per_card=2, stat_points=100
) -> List[Card]:
    """Method to init cards randomly (but with seed so not random), and shuffle them"""
    np.random.seed(GameConfig.seed)
    total_cards = player_count * cards_per_player
    card_list = []

    card_names = CardConfig.card_names  # TODO increase name pool?

    for idx in range(total_cards):
        generated_stats = random_stats(
            total_stats=stats_per_card, stat_points=stat_points
        )
        card_list.append(Card(name=card_names[idx], stats=generated_stats))

    np.random.shuffle(card_list)
    return card_list
