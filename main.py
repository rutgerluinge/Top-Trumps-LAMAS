import random

from game import Game
import cfg


# Main function obviously
def main():
    random.seed(cfg.RANDOM_SEED)
    topTrump = Game()

    # Start the game with default configuration
    topTrump.start_game(cfg.GameConfig())
    print(str(topTrump))
    if topTrump.has_winner():
        winner = topTrump.game_winner()
        print(
            f"{winner.name} has won the game with a score of {topTrump.scores[winner]}"
        )
    else:
        print("The game ended without a winner (tie)")


if __name__ == "__main__":
    main()
