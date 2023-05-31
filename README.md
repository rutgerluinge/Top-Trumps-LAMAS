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

### game.py
Main game class, handling most of the game.

### cfg.py
Settings file with all global parameters

### classes.py
Contains both the player class and the card class

### utils.py
Helper functions not belonging to a class

### cards.json
A json file with card data, expand this file to add more cards to the game.
