import mesa
import game
import classes
import random
import cfg


# mesa player class wrapper
class PlayerAgent(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model) -> None:
        super().__init__(unique_id, model)
        self.player = classes.Player()


# mesa driven model
class TopTrumpsModel(mesa.Model):
    # by default creates a game with default settings
    def __init__(self) -> None:
        self.from_config(cfg.GameConfig())

    # initialize a game with configuration
    def from_config(self, config: cfg.GameConfig):
        super().__init__(self)
        self.game = game.Game()
        self.game.initializeGame(config)
        return self

    # plays a single round of top trumps and updates the state
    def step(self):
        playedCards, winner = self.game.playRound()
        self.game.updateGameState(playedCards, winner)


# main function to play a game as a mesa server
def main():
    random.seed(cfg.RANDOM_SEED)
    model = TopTrumpsModel()
    model.game.print()
    while not model.game.hasWinner():
        model.step()


if __name__ == "__main__":
    main()
