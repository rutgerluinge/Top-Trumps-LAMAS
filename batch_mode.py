from mesa.batchrunner import batch_run
import mesa_model as mdl
import cfg


def main():
    # use default settings for now
    config = cfg.GameConfig()
    # DO NOTE: Random generators are currently configured outside of the model
    # This works, but if the batch_run can run in different order, the results
    # will not be consistent with equal seeds. AFAIK this is not the case, so it's good
    cfg.global_configuration(config)

    # Example: two configurations, one default, other with more players
    config_two = cfg.GameConfig()
    config_two.player_count = 4
    config_two.game_mode = cfg.GameMode.EPISTEMIC_POINT_LIMIT

    # start the batch
    batch_run(
        mdl.TopTrumpsModel,
        # here, each parameter (config) set is passed in a list
        parameters={"config": [config, config_two]},
        # each configuration combination is run up to this number of times
        iterations=config.batch_mode_run_limit,
    )


if __name__ == "__main__":
    main()
