from dataclasses import dataclass

# Set parameters here.

# Global parameters. TODO: set adjustable on front end.
from typing import List

PLAYER_COUNT = 3
STATS_COUNT = 3  # Equal to or lower than the amount of stats specified in cards.json
CARD_PER_PLAYER = 3  # Will be overwritten if there are less cards declared in cards.json   //changed this to cards per player less error prone

# Behind the screens parameters
RANDOM_SEED = 3
DEBUG = False
HARDCODED_CARD_NAMES = ["Chandler", "Monica", "Ross", "Phoebe", "Rachel", "Joey", "Janice", "Gunther", "Mr. Heckles", "Ursula", "Julie"]
HARDCODED_STAT_NAMES = ["Intelligence", "Charisma", "Looks", "Strength", "Game has not started a round!"]
STAT_POINTS = 100

@dataclass
class CardConfig:
    card_names = HARDCODED_CARD_NAMES
    stat_names = HARDCODED_STAT_NAMES


@dataclass
class GameConfig:
    player_count: int = PLAYER_COUNT  # n
    stats_count: int = STATS_COUNT  # m
    cards_pp: int = CARD_PER_PLAYER  # l
    seed: int = RANDOM_SEED
    debug: bool = DEBUG
    card_count: int = CARD_PER_PLAYER * PLAYER_COUNT
    stat_points: int = STAT_POINTS