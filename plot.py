import matplotlib.pyplot as plt

players = []
cards = []
strategies = []
winrates = []
stats = []

# Read all info from the results.txt file
with open("results.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        elements = line.split(" ")
        if elements[0] == "Players:":
            players.append(int(elements[1]))
            cards.append(int(elements[3]))
            strategies.append(elements[5])
            stats.append(int(elements[7][:-1]))
        elif len(elements) > 1 and elements[1] == "0":
            winrates.append(float(elements[2][:-1]) / 100)

x = [3,4,5,6]
y = []

for _ in range(0,27):
    y.append([])

# Loop through all info in results and put them in the right y list
for player, card, strategy, winrate, stat in zip(players, cards, strategies, winrates, stats):
    
    if strategy == "Smart":
        y[(player - 2) * 9 + ((stat - 2) * 3)].append(winrate)
    elif strategy == "Random":
        y[(player - 2) * 9 + ((stat - 2) * 3) + 1].append(winrate)
    elif strategy == "Highest_stat":
        y[(player - 2) * 9 + ((stat - 2) * 3) + 2].append(winrate)

# Two player plot
for i in range(0,3):
    plt.title("Win rate of one smart agent in a" + str(i + 2) + " player game.")
    plt.xlabel("Cards per player")
    plt.ylabel("Winrate (%) of the smart player")
    plt.ylim(0,100)
    plt.plot(x, y[i * 9 + 0], label="2 stats, Smart")
    plt.plot(x, y[i * 9 + 1], label="2 stats, Random")
    plt.plot(x, y[i * 9 + 2], label="2 stats, Highest stat")
    plt.plot(x, y[i * 9 + 3], label="3 stats, Smart")
    plt.plot(x, y[i * 9 + 4], label="3 stats, Random")
    plt.plot(x, y[i * 9 + 5], label="3 stats, Highest stat")
    plt.plot(x, y[i * 9 + 6], label="4 stats, Smart")
    plt.plot(x, y[i * 9 + 7], label="4 stats, Random")
    plt.plot(x, y[i * 9 + 8], label="4 stats, Highest stat")
    plt.legend()
    plt.show()

    plt.clf()
            