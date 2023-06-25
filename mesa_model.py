import mesa
import cfg
from top_trumps_model import TopTrumpsModel, run_to_completion
from model_renderer import RenderState, RenderKnowledge


# main function to play a game as a mesa server
def main():
    config = cfg.GameConfig()
    cfg.global_configuration(config)

    # run and output to CLI
    model = TopTrumpsModel(config)
    run_to_completion(model)

    # reset the game
    cfg.global_configuration(config)

    # run as a server with rudimentary visualization
    server = mesa.visualization.ModularServer(
        TopTrumpsModel,
        [RenderState(), RenderKnowledge()],
        "Top Trumps: Friends Edition",
    )
    server.launch()


if __name__ == "__main__":
    main()
