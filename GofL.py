from time import asctime, sleep
from os import path as findpath
import pygame as pyg
from tkinter import filedialog as fd
from numba import njit
import atexit
import numpy

#
#=-   Packages   -=#
"""

 * Pygame >= 2.1.2
 * Numba >= 0.55
 * Numpy >= 1.21, < 1.22
 * Tkinter

"""
#=-   ---===---   -=#
#


pyg.init()

#
#=-   My Logging Levels   -=#
"""

+--------------------+--------------------+--------------------+
| Level name         | Severity value     | Decorator          |
+====================+====================+====================+
| ZERO_LVL           | 0                  | {user_input}       |
+--------------------+--------------------+--------------------+
| DEBUG              | 10                 | '-_-'              |
+--------------------+--------------------+--------------------+
| INFO               | 20                 | '---'              |
+--------------------+--------------------+--------------------+
| WARNING            | 30                 | '-=-'              |
+--------------------+--------------------+--------------------+
| ERROR              | 40                 | '-!-'              |
+--------------------+--------------------+--------------------+
| CRITICAL           | 50                 | '!!!'              |
+--------------------+--------------------+--------------------+

"""
#=-   ---===---   -=#
#

#
#=-   Variables Types   -=#

# None


# Colors (other)
WH_c = (254, 254, 254)  # <- Cell dead color (254, 254, 254) default
BL_c = (0, 0, 0)  # <- Cell live color (0, 0, 0) default
GW_c = (204, 204, 204)  # <- Grid background color (204, 204, 204) default
GM_c = (144, 144, 144)   # <- Grid Trim color (144, 144, 144) default
GB_c = (84, 84, 84)

# Bool
Game_Status = 1
EDITING = 1
GRID = 1   # <- True by default
TRIM = 1   # <- True by default
LOG_DISABLED = 0   # <- False by default

# Int
Steps = 0
FPS = 60   # default: 60
EDITING_FPS = 10   # default: 10
BASE_CELL_SIZE = 12   # default: 12
X_Offset, Y_Offset = 2, 2   # default: 2, 2
Cells_Was, Cells_Left, Cells_Born, Cells_Died = 0, 0, 0, 0
FPS_REDUCE_STEP, FPS_RAISE_STEP = 5, 5   # default: 5, 5
FPS_MIN, FPS_MAX = 5, 255   # default: 5, 255
LOG_MIN_LVL = -1   # default: -1 (without minimal log_lvl)

# Str
MAIN_GAME_NAME = "Game of Life"
WDPath = findpath.abspath(findpath.dirname(__file__))
BASE_LOG_MODE = "a"   # default: "a"

# List


# Tuple
FILE_TYPES = (("All", "*.*"), ("TXT", "*.txt"), ("CSV", "*.csv"))

"""
^^^ default: ("All", "*.*"), ("TXT", "*.txt"), ("CSV", "*.csv")
"""

LOG_MODES = ("a", "w", "bw", "ba")   # default: ("a", "w", "bw", "ba")

# Dict
COLOR_PALETTE = {"cell_live": BL_c, "cell_dead": WH_c, "grid": GM_c, "trim": GW_c}

"""
^^^ default: {"cell_live": BL_c, "cell_dead": WH_c, "grid": GM_c, "trim": GW_c}
"""

KEY_BINDINGS = {"exit": pyg.K_ESCAPE, "start": (pyg.K_KP_ENTER, pyg.K_RETURN), "pause": pyg.K_SPACE,
                "minus": (pyg.K_MINUS, pyg.K_KP_MINUS), "plus": (pyg.K_PLUS, pyg.K_EQUALS, pyg.K_KP_PLUS),
                "import": pyg.K_o, "export": pyg.K_s, "grid_switch": pyg.K_g, "trim_switch": pyg.K_t}

"""
^^^ default: {"exit": pyg.K_ESCAPE, "start": (pyg.K_KP_ENTER, pyg.K_RETURN), "pause": pyg.K_SPACE,
              "minus": (pyg.K_MINUS, pyg.K_KP_MINUS), "plus": (pyg.K_PLUS, pyg.K_EQUALS, pyg.K_KP_PLUS),
              "import": pyg.K_o, "export": pyg.K_s, "grid_switch": pyg.K_g, "trim_switch": pyg.K_t}
"""

# Other


#=-   ---===---   -=#
#

#
#=-   Classes   -=#

#=-   ---===---   -=#
#

#
#=-   Global functions   -=#
def log_write(msg:str, log_lvl:int, end_of_msg:str="\n", start_of_msg:str="",
              zero_log_decorator:str="", between_part:str="   ", log_mode:str="a"):
    """
    Writes log messege with custom args

    ------
    Params:
    * msg : |str| - Messege
    * log_lvl : |int| - See LVLs below
    * end_of_msg : |str| = ("\\n") - Prefix for end of line
    * start_of_msg : |str| = ("") - Suffix for end of line
    * zero_log_decorator : |str| = ("") - User decorator for ZERO_LVL
    * between_part : |str| = ("   ") - Part between @msg and @lvl_part
    * log_mode : |str| = ("a") - Mode for current log messege

    ---
    LVLs:
    +--------------------+--------------------+--------------------+
    | Level name         | Severity value     | Decorator          |
    +====================+====================+====================+
    | ZERO_LVL           | 0                  | {user_input}       |
    +--------------------+--------------------+--------------------+
    | DEBUG              | 10                 | '-_-'              |
    +--------------------+--------------------+--------------------+
    | INFO               | 20                 | '---'              |
    +--------------------+--------------------+--------------------+
    | WARNING            | 30                 | '-=-'              |
    +--------------------+--------------------+--------------------+
    | ERROR              | 40                 | '-!-'              |
    +--------------------+--------------------+--------------------+
    | CRITICAL           | 50                 | '!!!'              |
    +--------------------+--------------------+--------------------+
    """

    if LOG_DISABLED or log_lvl <= LOG_MIN_LVL:
        return

    try:
        # Checks
        if (log_lvl > 60 or log_lvl < 0 or log_lvl % 10 != 0):
            log_lvl = 0
            log_write("Invallid Log LVL", 40)
            log_write("Log LVL switched to: 0", 30)

        if log_mode not in LOG_MODES:
            log_mode = "a"
            log_write("Invallid Log mode", 40)
            log_write("Log mode switched to: 'a'", 30)

        switch = {
            0: zero_log_decorator,
            10: "-_-",
            20: "---",
            30: "-=-",
            40: "-!-",
            50: "!!!",
        }

        lvl_part = switch.get(log_lvl, zero_log_decorator)

        with open(f'{WDPath}/Results.log', log_mode) as log_file:
            log_file.write(start_of_msg + lvl_part + between_part + msg + between_part + lvl_part + end_of_msg)

    except:
        return


def window_init():
    """
    Creates main display
    """
    global WINDOW, DISP_WIDTH, DISP_HEIGHT

    # Window preset
    try:
        DISP_WIDTH, DISP_HEIGHT = pyg.display.get_desktop_sizes()[0][0], pyg.display.get_desktop_sizes()[0][1]
    
    except:
        log_write("Failed to get Display Size", 40, start_of_msg="\n")
        log_write("Use default values (1280, 1024)", 30, end_of_msg="\n\n")
        DISP_WIDTH, DISP_HEIGHT = 1280, 1024

    WINDOW = pyg.display.set_mode((DISP_WIDTH, DISP_HEIGHT), pyg.DOUBLEBUF | pyg.HWSURFACE | pyg.FULLSCREEN |pyg.NOFRAME)
    pyg.display.set_caption("Conways "+ MAIN_GAME_NAME)
    pyg.display.set_icon(pyg.image.load(f'{WDPath}/GofL_logo.png', "Game_logo"))

    # Grid creation
    build_grid(BASE_CELL_SIZE, X_Offset, Y_Offset)


def build_grid(cell_size:int, x_offset:int, y_offset:int):
    """
    Fills screen by {grid} color\n
    Creates and displays cells array

    ------
    Params:
    * cell_size : |int|   - Cell size in pixels
    * x_offset : |int|   - Offset pixels from the left corner
    * y_offset : |int|   - Offset pixels from the top corner
    """
    global GRID, TRIM, X_CELLS, Y_CELLS, X_Offset, Y_Offset, Cells_Array, CELL_SIZE, TILE_SISE

    WINDOW.fill(COLOR_PALETTE['grid'])
    GRID, TRIM = 1, 1
    CELL_SIZE = cell_size
    TILE_SISE = CELL_SIZE + 1
    X_CELLS = (DISP_WIDTH -x_offset) // TILE_SISE
    Y_CELLS = (DISP_HEIGHT -y_offset) // TILE_SISE
    X_Offset, Y_Offset = x_offset, y_offset
    Cells_Array = numpy.zeros((Y_CELLS, X_CELLS), dtype=numpy.uint8)

    print_frame()


def print_frame():
    """
    Prints all cells on screen
    """

    for y in range(Y_CELLS):
        for x in range(X_CELLS):
            print_cell(x, y, Cells_Array[y, x])

    pyg.display.update()


def print_cell(x:int, y:int, st:int):
    """
    Prints only one cell

    ------
    Params:
    * x : |int|   - x of cell in Cells_Array
    * y : |int|   - y of cell in Cells_Array
    * st : |int|   - State of cell
    """

    rect = ((x * TILE_SISE) +X_Offset, (y * TILE_SISE) +Y_Offset, CELL_SIZE, CELL_SIZE)

    if st == 1:
        pyg.draw.rect(WINDOW, COLOR_PALETTE['cell_live'], rect)
    elif TRIM and st == 2:
        pyg.draw.rect(WINDOW, COLOR_PALETTE['trim'], rect)
    else:
        pyg.draw.rect(WINDOW, COLOR_PALETTE['cell_dead'], rect)


def set_cell(mouse_x:int, mouse_y:int, mode:bool):
    """
    If cell is dead  ->  makes it alive\n
    Elif cell is alive  ->  makes it dead

    ------
    Params:
    * m_x : |int|   - x of mouse position
    * m_y : |int|   - y of mouse position
    * mode : |bool|   - Mode of painting
    """
    global Cells_Was, Cells_Array

    x = mouse_x // TILE_SISE
    y = mouse_y // TILE_SISE

    try:
        Cells_Array[y, x]

        if mode and not(Cells_Array[y, x]):
            Cells_Array[y, x] = 1
            Cells_Was += 1
            print_cell(x, y, 1)

        elif not mode and Cells_Array[y, x]:
            Cells_Array[y, x] = 0
            Cells_Was -= 1
            print_cell(x, y, 0)

    except:
        log_write("Can't set cell on this place", 30)

def set_paused():
    """
    Sets program to paused state until [SPACE] is pressed
    """
    global Game_Status

    log_write(f"Paused!    Step: {Steps}", 20)
            
    pyg.display.set_caption(f"{str(pyg.display.get_caption()[0])} (Paused)")
    PAUSED = 1

    while PAUSED:
        for even in pyg.event.get():
            if even.type == pyg.KEYDOWN:
                if even.key == KEY_BINDINGS['pause']:
                    Game_Status = 1
                    PAUSED = 0 
                elif even.key == KEY_BINDINGS['exit']:
                    Game_Status = 0
                    PAUSED = 0

            elif even.type == pyg.QUIT:
                Game_Status = 0
                PAUSED = 0

        clock.tick(EDITING_FPS)

    log_write("Not Paused", 20)

    pyg.display.set_caption(str(pyg.display.get_caption()[0]).removesuffix(" (Paused)"))


def import_file():
    """
    Imports preset file and creates a new list of cells\n
    Prints all cells
    """
    global Cells_Array, Cells_Was, Cells_Left, X_Offset, Y_Offset

    try:
        log_write("Trying to load a preset file...", 10)

        with fd.askopenfile("r", title="Import a file", initialfile="GofL_preset.csv", initialdir=WDPath, filetypes=FILE_TYPES) as preset_file:
            preset_file.seek(0)

            meta_data = (preset_file.readline().removesuffix("\n")).split(",")
            build_grid(int(meta_data[0]), int(meta_data[1]), int(meta_data[2]))

            Cells_Array = numpy.genfromtxt(preset_file, dtype=numpy.uint8, delimiter=",", skip_header=0, encoding="UTF-8")
            Cells_Was = numpy.count_nonzero(Cells_Array == 1)
            Cells_Left = Cells_Was

        print_frame()
        log_write("Preset file successful imported", 20, end_of_msg="\n\n")

    except Exception as exp:
        log_write(f"Failed to import a preset file: {exp}", 40, end_of_msg="\n\n")


def export_file():
    """
    Exports preset to CSV file
    """

    try:
        log_write("Trying to export a preset file...", 10)

        with fd.asksaveasfile("w", title="Export a file", initialfile="GofL_preset.csv", initialdir=WDPath, filetypes=FILE_TYPES) as preset_file:
            preset_file.seek(0)

            preset_file.write(f"{CELL_SIZE},{X_Offset},{Y_Offset}")
            [preset_file.write(f'\n{",".join(list(map(lambda c: str(c), cells_row)))}') for cells_row in Cells_Array.tolist()]

        log_write("Preset file successful exported", 20, end_of_msg="\n\n")

    except Exception as exp:
        log_write(f"Failed to import a preset file: {exp}", 40, end_of_msg="\n\n")


@njit(fastmath=True)
def neighbors_check(old_cells_array, new_cells_array, CLeft:int, CBorn:int, CDied:int) -> tuple:
    """
    Checks neighbors for each cell inside 3x3 radius\n
    Returns new cells array and list with cells to update

    ---
    Params:
    * old_cells_array : |NumPy.Array|   - Array of cells with current states
    * new_cells_array : |NumPy.Array|   - Copy of @old_cells_array
    * CLeft : |int|   - Live cells amount
    * CBorn : |int|   - Borned cells amount
    * CDied : |int|   - Dead cells amount

    ---
    Return (tuple):
    * new_cells_array : |NumPy.Array|   - Array of cells with new states
    * draw_list : |list|   - List of cells to update
    * CLeft : |int|   - New live cells amount
    * CBorn : |int|   - New borned cells amount
    * CDied : |int|   - New dead cells amount

    ---
    Rules:

     If cell is alive:
      * Has 2 or 3 live neighbors  ->  Cell is staying alive
      * Else has < 2 or > 3 live neighbors  ->  Cell will be died

     Else if cell is dead:
      * Has 3 live neighbors  ->  Cell will be become alive
      * Else  ->  Cell is staying dead
    """

    draw_list = []

    for y in range(Y_CELLS):
        for x in range(X_CELLS):

            # Nearby cells inside 3x3 radius
            counter = 0

            for neighbor_cell_y in (y - 1, y, y + 1):
                if (neighbor_cell_y >= 0) and (neighbor_cell_y < Y_CELLS):

                    for neighbor_cell_x in (x - 1, x, x + 1):
                        if (neighbor_cell_x >= 0) and (neighbor_cell_x < X_CELLS):

                            if old_cells_array[neighbor_cell_y, neighbor_cell_x] == 1:
                                counter += 1

            #  Check results
            st = 0

            if old_cells_array[y, x] == 1:
                counter -= 1
                if counter == 2 or counter == 3:
                    st = 1

                else:
                    CLeft -= 1
                    CDied += 1
                    st = 2
                    draw_list.append((x, y, 2))

            else:
                if counter == 3:
                    CLeft += 1
                    CBorn += 1
                    st = 1
                    draw_list.append((x, y, 1))

                elif old_cells_array[y, x] != 0:
                    st = 2

            new_cells_array[y, x] = st

    return (new_cells_array, draw_list, CLeft, CBorn, CDied)


def hotkeys_check(event):
    """
    Checks all global events (hotkeys)

    ---
    Params:
    * event : |pygame.Event| - current event list to check

    ---
    Description

    ---
    If [ESC] key has been pressed or program has been closed -> to end a simulation (Game_Status to 0)\n
    Elif [ENTER] key has been pressed  ->  to start a simulation (EDITING to 0)

    ---
    Elif [SPACE] key has been pressed  ->  set_paused()

    ---
    Elif [-] key has been pressed  ->  to reduce FPS by FPS_REDUCE_STEP\n
    Elif [+] key has been pressed  ->  to raise FPS by FPS_RAISE_STEP

    ---
    Elif [Ctrl-O] hotkey has been pressed  ->  to import a preset file\n
    Elif [Ctrl-S] hotkey has been pressed  ->  to export a preset file

    ---
    Elif [Ctrl-G] hotkey has been pressed  ->  to switch GRID\n
    Elif [Ctrl-T] hotkey has been pressed  ->  to switch TRIM
    """

    global Game_Status, GRID, TRIM, EDITING, Cells_Left, FPS
    #REDUCING_FPS, RAISING_FPS

    #  Hot keys  #
    if event.type == pyg.KEYDOWN:
        # End
        if event.key == KEY_BINDINGS['exit']:
            Game_Status = 0

        #  Start simulation
        elif EDITING and event.key in KEY_BINDINGS['start']:
            EDITING = 0
            Cells_Left = Cells_Was
            pyg.display.set_caption(f"{MAIN_GAME_NAME} - View mode")


        # Pause
        elif not EDITING and event.key == KEY_BINDINGS['pause']:
            set_paused()


        # Reduce / Raise speed
        elif event.key in KEY_BINDINGS['minus']:
            FPS -= FPS_REDUCE_STEP
            if FPS < FPS_MIN:
                log_write("Min FPS limit reached", 10)
                FPS = 1

        elif event.key in KEY_BINDINGS['plus']:
            FPS += FPS_RAISE_STEP
            if FPS > FPS_MAX:
                log_write("Max FPS limit reached", 10)
                FPS = FPS_MAX
            elif FPS == FPS_RAISE_STEP+1:
                FPS = FPS_RAISE_STEP


        # Import / Export file
        elif pyg.KMOD_CTRL:
            if EDITING and event.key == KEY_BINDINGS['import']:
                import_file()

            elif EDITING and event.key == KEY_BINDINGS['export']:
                export_file()


            # GRID switch
            elif event.key == KEY_BINDINGS['grid_switch']:
                GRID = not GRID
                WINDOW.fill(COLOR_PALETTE['grid'] if GRID else COLOR_PALETTE['cell_dead'])

                log_write(f"Grid: {GRID}    Step: {Steps}", 20)
                print_frame()


            # TRIM switch
            elif not EDITING and event.key == KEY_BINDINGS['trim_switch']:
                TRIM = not TRIM
                print_frame()

                log_write(f"Trim: {TRIM}    Step: {Steps}", 20)


    elif event.type == pyg.QUIT:
        Game_Status = 0


#=-   ---===---   -=#
#


######
#=-   MAIN LOOPS   -=#
if __name__ == "__main__":

    log_write(asctime(), 30, end_of_msg="\n\n", start_of_msg="\n", log_mode=BASE_LOG_MODE)

    window_init()
    clock = pyg.time.Clock()
    pyg.display.set_caption(f"{MAIN_GAME_NAME} - Edit mode")

    #  Editing process  #

    while Game_Status and EDITING:

        # Check game status
        for event in pyg.event.get():
            hotkeys_check(event)

            # Set cell
            if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                PAINTING = 1

                try:
                    x = pyg.mouse.get_pos()[0] // TILE_SISE
                    y = pyg.mouse.get_pos()[1] // TILE_SISE
                    mode = 0 if Cells_Array[y, x] else 1

                except:
                    log_write("Failed to set painting mode", 40)
                    break

                while PAINTING:

                    for even in pyg.event.get():
                        if even.type == pyg.MOUSEBUTTONUP:
                            PAINTING = 0
                            break

                        elif even.type == pyg.MOUSEMOTION:
                            PAINTING = 1

                    set_cell(pyg.mouse.get_pos()[0], pyg.mouse.get_pos()[1], mode)
                    pyg.display.update()

        clock.tick(EDITING_FPS)


    #  Simulation process  #

    while Game_Status and Cells_Left > 0:

        # Check game status
        for evn in pyg.event.get():
            hotkeys_check(evn)

        # Check neighbors and create new real live list
        Cells_Array, CellsToDraw, Cells_Left, Cells_Born, Cells_Died =\
        neighbors_check(Cells_Array, numpy.copy(Cells_Array), Cells_Left, Cells_Born, Cells_Died)

        [print_cell(c_x, c_y, st) for c_x, c_y, st in CellsToDraw]
        pyg.display.update()

        Steps += 1
        clock.tick(FPS)

    #   --=--   #
    #

    if not(Cells_Left):
        log_write("Cells are over", 30, end_of_msg="\n", start_of_msg="\n")
        sleep(0.5)


#=-   ---===---   -=#
#

#####
#####   END   #

    atexit.register(lambda:
        log_write(f"Steps     : {Steps}\nCells was : {Cells_Was}\nCells left: {Cells_Left}\n"
                  f"Cells all : {Cells_Born + Cells_Was}\nCells born: {Cells_Born}\nCells died: {Cells_Died}",
                  0, end_of_msg="\n\n\n", start_of_msg="\n\n", zero_log_decorator="", between_part=""))

    exit()

#####=-   ---===---   -=#
#####

########
