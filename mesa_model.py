import mesa
import game
import classes
import random
import cfg


# mesa player class wrapper
## NOTE: This class currently goes unused, with the model handling all of the functionality of the agents directly
class PlayerAgent(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model) -> None:
        super().__init__(unique_id, model)
        self.player = classes.Player()

    def step():
        # nothing needed just yet, model takes care of agents
        pass


# mesa driven model
class TopTrumpsModel(mesa.Model):
    # by default creates a game with default settings
    def __init__(self) -> None:
        self.from_config(cfg.GameConfig())
        # map datacollector to print functions
        self.datacollector = mesa.DataCollector(
            model_reporters={"State": self.game.to_string}
        )

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
        self.datacollector.collect(self)


# steps the model until there is a winner
def run_to_completion(model: TopTrumpsModel):
    while not model.game.hasWinner():
        model.step()


def to_html(input: str):
    # replace newlines with paragraph breaks (html)
    return input.replace("\n", "<br/>")


class RenderState(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()

    # renders the state of the game as text
    def render(self, model: TopTrumpsModel):
        # if the game has a winner, announce it
        if model.game.hasWinner():
            return str(
                "Game is over, " + model.game.playerList[0].name + "won the game!"
            )

        # render the current game state
        return to_html(model.game.to_string())


# main function to play a game as a mesa server
def main():
    random.seed(cfg.RANDOM_SEED)

    # example usages of the mesa classes

    # run and output to CLI
    model = TopTrumpsModel()
    model.game.print()
    run_to_completion(model)
    # print a summary of collected states
    states = model.datacollector.get_model_vars_dataframe()
    print(states)

    # run as a server with rudimentary visualization
    server = mesa.visualization.ModularServer(
        TopTrumpsModel, [RenderState()], "Top Trumps: Friends Edition"
    )
    server.launch()


if __name__ == "__main__":
    main()
