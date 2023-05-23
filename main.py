import random

from game import Game
import cfg


# Main function obviously
def main():
    random.seed(cfg.RANDOM_SEED)
    topTrump = Game()

    #Start the game
    topTrump.startGame()

if __name__=='__main__':
    main()