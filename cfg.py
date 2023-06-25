from dataclasses import dataclass
from enum import Enum
import random


# Set parameters here.

class StrategyEnum(Enum):
    RANDOMSTAT = 1

    HIGHSTAT = 2

    SMARTSTAT = 3


class GameMode(Enum):
    # Standard game mode (with slightly altered rules)
    STANDARD = 1
    ## Epistemic game modes (no card transfers)
    # Game mode with a limited number of rounds
    EPISTEMIC_ROUND_LIMIT = 2
    # Game mode where the winner is the first to a set number of points
    EPISTEMIC_POINT_LIMIT = 3


# Global parameters. TODO: set adjustable on front end.
PLAYER_COUNT = 3
STATS_COUNT = 2  # Equal to or lower than the amount of stats specified in cards.json
CARD_PER_PLAYER = 3  # Changed this to cards per player less error prone
FULL_ANNOUNCEMENT = True
GAME_MODE = GameMode.EPISTEMIC_ROUND_LIMIT
# maximum score or round number in epistemic game modes
MAX_ROUND_OR_SCORE = 10
# number of games to play when running the batch mode
BATCH_MODE_NUMBER_OF_RUNS = 10000

#
GENERATE_KRIPKE_MODEL = False

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
    max_round_or_score: int = MAX_ROUND_OR_SCORE
    generate_kripke: bool = GENERATE_KRIPKE_MODEL
    batch_mode_run_limit = BATCH_MODE_NUMBER_OF_RUNS
    smart_strategy: StrategyEnum = StrategyEnum.SMARTSTAT
    dummy_strategy: StrategyEnum = StrategyEnum.RANDOMSTAT


def global_configuration(config: GameConfig):
    """Global configuration actions. Run this to completely reset the environment"""
    random.seed(config.seed)
