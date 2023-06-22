from dataclasses import dataclass
from enum import Enum

# Set parameters here.


class GameMode(Enum):
    # Standard game mode (with slightly altered rules)
    STANDARD = 1
    # Epistemic game mode (no card transfers)
    EPISTEMIC = 2


# Global parameters. TODO: set adjustable on front end.
PLAYER_COUNT = 3
STATS_COUNT = 3  # Equal to or lower than the amount of stats specified in cards.json
CARD_PER_PLAYER = 3  # Changed this to cards per player less error prone
FULL_ANNOUNCEMENT = True
GAME_MODE = GameMode.EPISTEMIC

# Behind the screens parameters
RANDOM_SEED = 3
DEBUG = False
HARDCODED_CARD_NAMES = [
    "Chandler",
    "Monica",
    "Ross",
    "Phoebe",
    "Rachel",
    "Joey",
    "Janice",
    "Gunther",
    "Mr. Heckles",
    "Ursula",
    "Julie",
]
HARDCODED_STAT_NAMES = [
    "Intelligence",
    "Charisma",
    "Looks",
    "Strength",
    "Game has not started a round!",
]
STAT_POINTS = 100


@dataclass
class CardConfig:
    card_names = HARDCODED_CARD_NAMES
    stat_names = HARDCODED_STAT_NAMES


@dataclass
class GameConfig:
    game_mode: GameMode = GAME_MODE
    player_count: int = PLAYER_COUNT  # n
    stats_count: int = STATS_COUNT  # m
    cards_pp: int = CARD_PER_PLAYER  # l
    seed: int = RANDOM_SEED
    debug: bool = DEBUG
    card_count: int = CARD_PER_PLAYER * PLAYER_COUNT
    stat_points: int = STAT_POINTS
    full_announcement: bool = FULL_ANNOUNCEMENT
