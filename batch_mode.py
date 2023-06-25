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

    resultstxt = open("results.txt", "w+")
    # start the batch
    for players in range(2, 5):
        for cards in range(3, 7):
            for stat in range(2, 5):
                for strategy in range(0, 3):
                    config.player_count = players
                    config.cards_pp = cards
                    config.stats_count = stat
                    if strategy == 0:
                        resultstxt.write(
                            "Players: "
                            + str(players)
                            + " Cards: "
                            + str(cards)
                            + " Strategy: Smart Stat_count: "
                            + str(stat)
                            + "\n"
                        )
                        config.dummy_strategy = cfg.StrategyEnum.SMARTSTAT
                    elif strategy == 1:
                        resultstxt.write(
                            "Players: "
                            + str(players)
                            + " Cards: "
                            + str(cards)
                            + " Strategy: Highest_stat Stat_count: "
                            + str(stat)
                            + "\n"
                        )
                        config.dummy_strategy = cfg.StrategyEnum.HIGHSTAT
                    elif strategy == 2:
                        resultstxt.write(
                            "Players: "
                            + str(players)
                            + " Cards: "
                            + str(cards)
                            + " Strategy: Random Stat_count: "
                            + str(stat)
                            + "\n"
                        )
                        config.dummy_strategy = cfg.StrategyEnum.RANDOMSTAT
                    results = batch_run(
                        mdl.TopTrumpsModel,
                        # here, each parameter (config) set is passed in a list
                        parameters={"config": [config]},
                        # each configuration combination is run up to this number of times
                        iterations=config.batch_mode_run_limit,
                    )

                    # results captures the collected data from the model reporters. We summarize them here
                    win_counts = dict()
                    for result in results:
                        # names here map onto the defined data collectors of the model
                        winner = result["Winner"]
                        name = winner.name if winner != None else "Tie"
                        if name in win_counts:
                            win_counts[name] += 1
                        else:
                            win_counts[name] = 1

                    # print the number of games won for each player
                    # NOTE: this does combine player names from different configurations
                    # run only a single configuration OR differentiate the configurations in the
                    # DataCollector
                    if config.debug:
                        print(
                            "Players:",
                            players,
                            "Cards:",
                            cards,
                            "Strategies",
                            strategy,
                            "Statcount:",
                            stat,
                        )
                    for player in win_counts:
                        # in case of a tie, None will be reported as the winner
                        resultstxt.write(
                            str(player) + " " + str(win_counts[player]) + "\n"
                        )
                        if config.debug:
                            print(str(player) + " " + str(win_counts[player]))


if __name__ == "__main__":
    main()
