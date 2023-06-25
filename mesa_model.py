import mesa
import game
from agents import Player
import cards
import random
import cfg


# mesa player class wrapper
## NOTE: This class currently goes unused, with the model handling all of the functionality of the agents directly
class PlayerAgent(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model) -> None:
        super().__init__(unique_id, model)
        self.player = Player(name="dummy", card_list=[])

    def step(self):
        # nothing needed just yet, model takes care of agents
        pass


# mesa driven model
class TopTrumpsModel(mesa.Model):
    # by default creates a game with default settings
    def __init__(self) -> None:
        super().__init__(self)
        self.from_config(cfg.GameConfig())
        # map datacollector to print functions
        self.datacollector = mesa.DataCollector(
            model_reporters={"State": self.game.__str__}
        )

    # initialize a game with configuration
    def from_config(self, config: cfg.GameConfig):
        self.game = game.Game()
        self.game.initialize_game(config)
        return self

    # plays a single round of top trumps and updates the state
    def step(self):
        playedCards, winner, stat_idx = self.game.play_round()
        self.game.update_game_state(playedCards, winner, stat_idx)
        self.datacollector.collect(self)
        # automatically end a simulation if there is a winner
        if self.game.has_ended():
            self.running = False


# steps the model until there is a winner
def run_to_completion(model: TopTrumpsModel):
    while not model.game.has_ended():
        if model.game.config.generate_kripke:
            model.game.createKripkeModel()
        model.step()


def to_html(input: str):
    # replace newlines with paragraph breaks (html)
    html = input.replace("\n", "<br/>")
    return html


class RenderState(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()

    # renders the state of the game as text
    def render(self, model: TopTrumpsModel):
        # if the game has a winner, announce it
        if model.game.has_winner():
            return to_html(
                str(
                    "Game is over, "
                    + model.game.players_in_game()[1][0].get_name()
                    + " won the game!"  # todo error prone!
                )
                + f"\n Final state: \n\n {model.game.print_interface()}"
            )
        elif model.game.has_ended():
            return to_html(
                str(
                    "The game has ended without a winner!"
                    + f"\n Final state: \n\n {model.game.print_interface()}"
                )
            )

        # render the current game state
        return to_html(model.game.print_interface())


class RenderKnowledge(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()

    def render(self, model: TopTrumpsModel):
        knowledge = str()
        for agent in model.game.state.players:
            knowledge += "\n" + str(agent.agent_knowledge)
        return to_html(knowledge)


# main function to play a game as a mesa server
def main():
    random.seed(cfg.RANDOM_SEED)

    # example usages of the mesa classes

    # run and output to CLI
    model = TopTrumpsModel()
    run_to_completion(model)

    # run as a server with rudimentary visualization
    server = mesa.visualization.ModularServer(
        TopTrumpsModel,
        [RenderState(), RenderKnowledge()],
        "Top Trumps: Friends Edition",
    )
    server.launch()


if __name__ == "__main__":
    main()
