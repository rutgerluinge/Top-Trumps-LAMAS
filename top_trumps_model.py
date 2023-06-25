import mesa
import game
import cfg
from agents import Player


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
    def __init__(self, **kwargs) -> None:
        config = kwargs.get("config")
        self.__init__(config=config)

    # by default creates a game with default settings
    def __init__(self, config: cfg.GameConfig = cfg.GameConfig()) -> None:
        super().__init__(self)
        # we need a base scheduler just to comply with batch mode, not used
        self.schedule = mesa.time.BaseScheduler(self)
        self.from_config(config)
        # map datacollector to print functions
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "State": self.game.__str__,
                "Winner": self.game.game_winner,
                "Number of rounds": "self.game.round",
            }
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
