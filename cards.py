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


def init_cards(player_count=2, cards_per_player=2, stats_per_card=2, stat_points=100) -> List[Card]:
    """Method to init cards randomly (but with seed so not random), and shuffle them"""
    np.random.seed(GameConfig.seed)
    total_cards = player_count * cards_per_player
    card_list = []

    card_names = CardConfig.card_names  # TODO increase name pool?

    for idx in range(total_cards):
        generated_stats = random_stats(total_stats=stats_per_card, stat_points=stat_points)
        card_list.append(Card(name=card_names[idx], stats=generated_stats))

    np.random.shuffle(card_list)
    return card_list
