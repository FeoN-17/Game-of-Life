## Conway's Game of Life in Python

![LOGO](./GofL_logo.png)

#### The Game of Life, is a [cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton) devised by the British [mathematician](https://en.wikipedia.org/wiki/Mathematician) [John Horton Conway](https://en.wikipedia.org/wiki/John_Horton_Conway) in 1970. It is a [zero-player game](https://en.wikipedia.org/wiki/Zero-player_game), meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. It is [Turing complete](https://en.wikipedia.org/wiki/Turing_complete) and can simulate a [universal constructor](https://en.wikipedia.org/wiki/Von_Neumann_universal_constructor) or any other [Turing machine](https://en.wikipedia.org/wiki/Turing_machine).



#### Language: [Python 3.10](https://www.python.org/downloads/release/python-3102/)

#### Author: [FeoN_](https://github.com/FeoN-17?tab=repositories)

#### License: [Mozilla Public License Version 2.0](./LICENSE)

#### Wiki: [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)



### PACKAGES

* Python >= 3.10.2, < 3.11
* Pygame >= 2.1.2
* Numba >= 0.55
* Numpy >= 1.21, < 1.22
* Tkinter



### RUN

Just run file using Python 3

`python3 GofL.py`



### RULES

#### If cell is alive:

 * Has < 2 or > 3 live neighbors -> cell will be died
 * Else has 2 or 3 live neighbors -> cell is staying alive

#### Else if cell is dead:
 * Has 3 live neighbors -> cell will be become alive
 * Else -> cell is staying dead



### HOTKEYS

#### `ESC` or `[X] icon`:  to `end` a simulation

#### `ENTER`:  to `start` a simulation

#### `SPACE`:  to `pause` and `unpause` simulation



#### `+`:  to `raise` speed of simulation by 5 FPS

#### `-`:  to `reduce` speed of simulation by 5 FPS



#### `Ctrl-O`:  to `import` a preset file

#### `Ctrl-S`:  to `export` a preset file



#### `Ctrl-G`:  to switch `GRID` state

#### `Ctrl-T`:   to switch `TRIM` state



### FEATURES

* #### Save / Load preset files
* #### Raise / Reduce speed of simulation
* #### Editable color palette
* #### Painting mode
* #### Logging
* #### High performance using [Numba](https://numba.pydata.org/), machine code
