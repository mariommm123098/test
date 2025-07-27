# Guess the Number Game

This repository contains a small command-line game written in Python. The goal is to guess the random number selected by the program.

## Running the Game

To run the game, make sure you have Python 3 installed and execute:

```bash
python3 guess_game.py
```

## Building an Executable (optional)

If you want a standalone executable, you can use `pyinstaller`. First install it:

```bash
pip install pyinstaller
```

Then build the executable:

```bash
pyinstaller --onefile guess_game.py
```

The resulting executable can be found in the `dist` folder.
