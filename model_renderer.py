import mesa
from top_trumps_model import TopTrumpsModel
from formatting import *


class RenderState(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()

    # renders the state of the game as text
    def render(self, model: TopTrumpsModel):
        rendered_text = str()
        # if the game has a winner, announce it
        if model.game.has_winner():
            rendered_text += bold_face(
                f"Game is over, {model.game.players_in_game()[0].get_name()} won the game!\n"
            )
        elif model.game.has_ended():
            rendered_text += bold_face("The game has ended without a winner!\n")

        # render the current game state
        rendered_text += model.game.print_interface()
        return to_html(rendered_text)


class RenderKnowledge(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()

    def render(self, model: TopTrumpsModel):
        # render only a single knowledge state, as they are all equivalent
        knowledge = bold_face("Agent belief state\n")
        if len(model.game.state.players):
            knowledge += f"{model.game.state.players[0].agent_knowledge}"
        return to_html(knowledge)
