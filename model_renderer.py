import mesa
from top_trumps_model import TopTrumpsModel


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
                    + model.game.players_in_game()[0].get_name()
                    + " won the game!"
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
