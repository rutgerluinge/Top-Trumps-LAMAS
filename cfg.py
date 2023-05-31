from dataclasses import dataclass

# Set parameters here.

# Global parameters. TODO: set adjustable on front end.
PLAYER_COUNT = 2
STATS_COUNT = 2  # Equal to or lower than the amount of stats specified in cards.json
CARD_COUNT = 6  # Will be overwritten if there are less cards declared in cards.json

# Behind the screens parameters
RANDOM_SEED = 1
DEBUG = True


@dataclass
class GameConfig:
    player_count: int = PLAYER_COUNT  # n
    stats_count: int = STATS_COUNT  # m
    card_count: int = CARD_COUNT  # l
    seed: int = RANDOM_SEED
    debug: bool = DEBUG
