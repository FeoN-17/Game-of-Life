<h1 align="center"> Conway's Game of Life in Python </h1>
<p align="center"><img title="Game-of-Life" alt="LOGO" src='GofL_logo.png'/></p>

#### The Game of Life, is a [cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton) devised by the British [mathematician](https://en.wikipedia.org/wiki/Mathematician) [John Horton Conway](https://en.wikipedia.org/wiki/John_Horton_Conway) in 1970. It is a [zero-player game](https://en.wikipedia.org/wiki/Zero-player_game), meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. It is [Turing complete](https://en.wikipedia.org/wiki/Turing_complete) and can simulate a [universal constructor](https://en.wikipedia.org/wiki/Von_Neumann_universal_constructor) or any other [Turing machine](https://en.wikipedia.org/wiki/Turing_machine).

#### Now on Python! I hope you will use this program for data and/or computer science or just for fun!

<br>

#### Language: [Python 3.10.2](https://www.python.org/downloads/release/python-3102/)

#### Author: [FeoN_](https://github.com/FeoN-17?tab=repositories)

#### License: [Mozilla Public License Version 2.0](LICENSE)

#### Wiki: [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

<br>

-------
<br>
<br>

### [PACKAGES](requirements/)
______

* Python >= 3.10.2, < 3.11
* Pygame >= 2.1.2
* Numba >= 0.55
* NumPy >= 1.21, < 1.22
* Tkinter

<br>

For pip install packages from [`requirements.txt`](requirements/requirements.txt)

`pip install --upgrade -r ./requirements/requirements.txt`

<br>

For poetry:

1. Copy [`pyproject.toml`](requirements/pyproject.toml) or it is dependings to .venv or other env and update `poetry.lock` file
```bash
cp ./requirements/pyproject.toml /path/to/venv/ ; cd /path/to/venv/
poetry update
```

2. Or add dependings from [`poetry_deps.txt`](requirements/poetry_deps.txt) to your `pyproject.toml` and update. Only python >=3.10, <3.11
```bash
poetry add `cat Game-of-Life/requirements/requirement.txt`
poetry update
```

<br>
<br>

### RUN
______

#### Just run with Python3

```bash
python3 GofL.py
```

<br>
<br>

### RULES
______

#### If cell is alive:

 * Has < 2 or > 3 live neighbors -> cell will be died
 * Else has 2 or 3 live neighbors -> cell is staying alive

<br>

#### Else if cell is dead:

 * Has 3 live neighbors -> cell will be become alive
 * Else -> cell is staying dead

<br>
<br>

### HOTKEYS
______

#### `ESC` or `[X] icon`:  to `end` a simulation

#### `ENTER`:  to `start` a simulation

#### `SPACE`:  to `pause` and `unpause` simulation

<br>

#### `+`:  to `raise` speed of simulation by 5 FPS

#### `-`:  to `reduce` speed of simulation by 5 FPS

<br>

#### `Ctrl-O`:  to `import` a preset file

#### `Ctrl-S`:  to `export` a preset file

<br>

#### `Ctrl-G`:  to switch `GRID` state

#### `Ctrl-T`:   to switch `TRIM` state

<br>
<br>

### FEATURES
______

* #### Save / Load preset files

* #### Raise / Reduce speed of simulation

* #### Many editable elements in code (colors, keybindings)

* #### Painting mode

* #### Logging

* #### High performance using [Numba](https://numba.pydata.org/), machine code

<br>
<br>

### FUTURE
______

- [ ] **New hotkey binding system**
- [ ] **New logger**
- [ ] **Brushes files**
- [ ] **? Docker support ?**
- [ ] **Other**