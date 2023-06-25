import random

from game import Game
import cfg


# Main function obviously
def main():
    # use the default configuration
    config = cfg.GameConfig()
    cfg.global_configuration(config)

    # Start the game
    topTrump = Game()
    topTrump.start_game(config)
    
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
