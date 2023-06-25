# Top-Trumps-LAMAS
LAMAS course project about public statements in a simplified Top Trumps game!

### install required packages:
pip install -r requirements.txt

## running the model
### as a neutral cli application
```python main.py```

### as a mesa model
```python mesa_model.py```
This runs the model once and prints the output to stdout, then spawns a mesa server with a new model that can be interacted with.

## Files

### mesa_model.py
Contains mesa classes that encapsulate the game.

### main.py
The main file which starts everything

### batch_mode.py
Runs the model in batch mode, based on the default configured settings. Additional configurations can be added in this file to compare against the default.
### game.py
Main game class, handling most of the game.

### cfg.py
Settings file with all global parameters

### cards.py
contains the card class and more methods for card generation

### agent.py
contains the Player/agent class and will contain different behavior for different type
of agents.
### utils.py
Helper functions not belonging to a class

### cards.json
A json file with card data, expand this file to add more cards to the game.
