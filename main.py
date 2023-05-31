import random

from game import Game
import cfg


# Main function obviously
def main():
    random.seed(cfg.RANDOM_SEED)
    topTrump = Game()

    # Start the game with default configuration
    topTrump.startGame(cfg.GameConfig())


if __name__ == "__main__":
    main()
