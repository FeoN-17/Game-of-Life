import pygame as pyg
from tkinter import filedialog as fd
from numba import njit
from time import asctime, sleep
from os import path as findpath
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

   QUESTIONS=60    -?-   {msg}   -?-

   DEBUG=10    -_-   {msg}   -_-
   INFO=20    ---   {msg}   ---
   WARN=30    -=-   {msg}   -=-
   ERROR=40    -!-   {msg}   -!-
   CRITICAL=50    !!!   {msg}   !!!

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
FPS = 120   # <- default: 120
EDITING_FPS = 10   # <- default: 10
BASE_CELL_SIZE = 12   # <- default: 12 by
X_Offset, Y_Offset = 2, 2   # <- default: 2, 2
Cells_Was, Cells_Left, Cells_Born, Cells_Died = 0, 0, 0, 0

# Str
MAIN_GAME_NAME = "Game of Life"
WDPath = findpath.abspath(findpath.dirname(__file__))
BASE_LOG_MODE = "a"   # <- default: "a"

# List


# Tuple
FILE_TYPES = (("All", "*.*"), ("TXT", "*.txt"), ("CSV", "*.csv"))
# ^^^ default: ("All", "*.*"), ("TXT", "*.txt"), ("CSV", "*.csv")
LOG_MODES = ("a", "w", "bw", "ba")   # <- default: ("a", "w", "bw", "ba")

# Dict
COLOR_PALETTE = {"cell_live": BL_c, "cell_dead": WH_c, "grid": GM_c, "trim": GW_c}
# ^^^ default: {"cell_live": BL_c, "cell_dead": WH_c, "grid": GM_c, "trim": GW_c}
KEY_BINDINGS = {"exit": pyg.K_ESCAPE, "start": (pyg.K_KP_ENTER, pyg.K_RETURN), "pause": pyg.K_SPACE,
                "minus": (pyg.K_MINUS, pyg.K_KP_MINUS), "plus": (pyg.K_PLUS, pyg.K_EQUALS, pyg.K_KP_PLUS),
                "import": pyg.K_o, "export": pyg.K_s, "grid_switch": pyg.K_g, "trim_switch": pyg.K_t}
""" ^^^ default: {"exit": pyg.K_ESCAPE, "start": (pyg.K_KP_ENTER, pyg.K_RETURN), "pause": pyg.K_SPACE,
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

def log_write(msg:str, log_lvl:int, end_of_msg:str="\n", start_of_msg:str="", zero_log_prefix:str="", between_part:str="   ", log_mode:str="a"):

    if LOG_DISABLED:
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
            0: zero_log_prefix,
            10: "-_-",
            20: "---",
            30: "-=-",
            40: "-!-",
            50: "!!!",
            60: "-?-",
        }

        lvl_part = switch.get(log_lvl, zero_log_prefix)

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
        log_write("Display size couldn't executed", 40, start_of_msg="\n")
        log_write("Use default values (1280,1024)", 30, end_of_msg="\n\n")
        DISP_WIDTH, DISP_HEIGHT = 1280, 1024

    WINDOW = pyg.display.set_mode((DISP_WIDTH, DISP_HEIGHT), pyg.DOUBLEBUF | pyg.HWSURFACE | pyg.FULLSCREEN |pyg.NOFRAME)
    pyg.display.set_caption("Conways "+ MAIN_GAME_NAME)
    pyg.display.set_icon(pyg.image.load(f'{WDPath}/GofL_logo.png', "Game_logo"))

    # Grid creation
    build_grid(BASE_CELL_SIZE, X_Offset, Y_Offset)


def build_grid(cell_size:int, x_offset:int, y_offset:int):
    """
    Fills screen by {grid} color
    Creates and displays cells
    :param cell_size: cell size in pixels
    :param x_offset: offset pixels from the left corner
    :param y_offset: offset pixels from the top corner
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
    :param x: x of cell in Cells_Array
    :param y: y of cell in Cells_Array
    :param st: state for cell
    """

    rect = ((x * TILE_SISE) +X_Offset, (y * TILE_SISE) +Y_Offset, CELL_SIZE, CELL_SIZE)

    if st == 1:
        pyg.draw.rect(WINDOW, COLOR_PALETTE['cell_live'], rect)
    elif st == 2 and TRIM:
        pyg.draw.rect(WINDOW, COLOR_PALETTE['trim'], rect)
    else:
        pyg.draw.rect(WINDOW, COLOR_PALETTE['cell_dead'], rect)


def set_cell(mouse_x:int, mouse_y:int, mode:bool):
    """
    If cell is dead -> makes it alive
    Elif cell is alive -> makes it dead
    :param m_x: x of mouse position
    :param m_y: y of mouse position
    :param mode: mode of painting
    """
    global Cells_Was, Cells_Array

    x = mouse_x // TILE_SISE
    y = mouse_y // TILE_SISE

    try:
        Cells_Array[y, x]

        if not(Cells_Array[y, x]) and mode:
            Cells_Array[y, x] = 1
            Cells_Was += 1
            print_cell(x, y, 1)

        elif Cells_Array[y, x] and not(mode):
            Cells_Array[y, x] = 0
            Cells_Was -= 1
            print_cell(x, y, 0)

    except:
        log_write("Can't set cell on this place", 30)


def import_file():
    """
    Imports preset file and creates a new list of cells
    Prints all cells
    """
    global Cells_Array, Cells_Was, Cells_Left, X_Offset, Y_Offset

    try:
        log_write("Trying to load a preset file...", 30)

        with fd.askopenfile("r", title="Import a file", initialfile="GofL_preset.csv", initialdir=WDPath, FILE_TYPES=FILE_TYPES) as preset_file:
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
        log_write("Trying to export a preset file...", 30)

        with fd.asksaveasfile("w", title="Export a file", initialfile="GofL_preset.csv", initialdir=WDPath, FILE_TYPES=FILE_TYPES) as preset_file:
            preset_file.seek(0)

            preset_file.write(f"{CELL_SIZE},{X_Offset},{Y_Offset}")
            [preset_file.write(f'\n{",".join(list(map(lambda c: str(c), cells_row)))}') for cells_row in Cells_Array.tolist()]

        log_write("Preset file successful exported", 20, end_of_msg="\n\n")

    except Exception as exp:
        log_write(f"Failed to import a preset file: {exp}", 40, end_of_msg="\n\n")


@njit(fastmath=True)
def neighbors_check(old_cells_list, new_cell_list, CLeft:int, CBorn:int, CDied:int):
    """
    Checks neighbors for each cell inside 3x3 radius

    Rules:
     If cell is alive:
      * Has fewer than 2 or more than 3 live neighbors   ->   cell will be died
      * Else has 2 or 3 live neighbors   ->   cell is staying alive

     Else if cell is dead:
      * Has 3 live neighbors   ->   cell will be become alive
      * Else   ->   cell is staying dead
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

                            if old_cells_list[neighbor_cell_y, neighbor_cell_x] == 1:
                                counter += 1

            #  Check results
            st = 0

            if old_cells_list[y, x] == 1:
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

                elif old_cells_list[y, x] != 0:
                    st = 2

            new_cell_list[y, x] = st

    return (new_cell_list, draw_list, CLeft, CBorn, CDied)


def global_events_check(event):
    """
    If =ESC= key or [X] icon has been pressed -> to end a simulation
    Elif =ENTER= key has been pressed -> to start a simulation

    Elif =SPACE= key has been pressed:
     * 1. While =SPACE= hasn't been pressed again -> to pause a simulation
     * 2. When =SPACE= has been pressed again -> to unpause a simulation

    ElIf =-= key has been pressed -> to reduce FPS by 5
    ElIf =+= key has been pressed -> to raise FPS by 5

    ElIf =Ctrl-O= hotkey has been pressed -> to import a preset file
    ElIf =Ctrl-S= hotkey has been pressed -> to export a preset file

    ElIf =Ctrl-G= hotkey has been pressed -> to switch GRID
    ElIf =Ctrl-T= hotkey has been pressed -> to switch TRIM
    """

    global Game_Status, GRID, TRIM, EDITING, Cells_Left, FPS

    #  Hot keys  #
    if event.type == pyg.KEYDOWN:
        # End
        if event.key == KEY_BINDINGS['exit']:
            Game_Status = 0

        #  Start simulation
        elif event.key in KEY_BINDINGS['start'] and EDITING:
            EDITING = 0
            Cells_Left = Cells_Was
            pyg.display.set_caption(f"{MAIN_GAME_NAME} - View mode")


        # Pause
        elif event.key == KEY_BINDINGS['pause'] and not(EDITING):

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


        # Speed Up / Down
        elif event.key in KEY_BINDINGS['minus']:
            FPS -= 5
            if FPS < 5:
                FPS = 1

        elif event.key in KEY_BINDINGS['plus'] and FPS < 255:
            FPS += 4 if FPS == 1 else 5


        # Import / Export file
        elif pyg.KMOD_CTRL:
            if event.key == KEY_BINDINGS['import'] and EDITING:
                import_file()

            elif event.key == KEY_BINDINGS['export'] and EDITING:
                export_file()


            # GRID switch
            elif event.key == KEY_BINDINGS['grid_switch']:
                GRID = not GRID
                WINDOW.fill(COLOR_PALETTE['grid'] if GRID else COLOR_PALETTE['cell_dead'])

                log_write(f"Grid: {GRID}\tStep: {Steps}", 20)
                print_frame()


            # TRIM switch
            elif event.key == KEY_BINDINGS['trim_switch'] and not(EDITING):
                TRIM = not TRIM
                print_frame()

                log_write(f"Trim: {TRIM}\tStep: {Steps}", 20)

    elif event.type == pyg.QUIT:
        Game_Status = 0


#=-   ---===---   -=#
#


######
#=-   MAIN LOOPS   -=#
if __name__ == "__main__":

    log_write(f"-Results of simulation (Date: {asctime()})-", 30, end_of_msg="\n\n", start_of_msg="\n", log_mode=BASE_LOG_MODE)

    window_init()
    clock = pyg.time.Clock()
    pyg.display.set_caption(f"{MAIN_GAME_NAME} - Edit mode")

    #  Editing process  #

    while Game_Status and EDITING:

        # Check game status
        for event in pyg.event.get():
            global_events_check(event)

            # Set cell
            if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                PAINTING = 1

                try:
                    x = pyg.mouse.get_pos()[0] // TILE_SISE
                    y = pyg.mouse.get_pos()[1] // TILE_SISE
                    mode = 0 if Cells_Array[y, x] else 1

                except:
                    log_write(f"Failed to set painting mode", 40)
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
            global_events_check(evn)

        # Check neighbors and create new real live list
        Cells_Array, CellsToDraw, Cells_Left, Cells_Born, Cells_Died = neighbors_check(Cells_Array, numpy.copy(Cells_Array), Cells_Left, Cells_Born, Cells_Died)

        [print_cell(c_x, c_y, st) for c_x, c_y, st in CellsToDraw]
        pyg.display.update()

        Steps += 1
        clock.tick(FPS)

    #   --=--   #
    #

    if not(Cells_Left):
        log_write(f"Cells are over ", 30, end_of_msg="\n", start_of_msg="\n")
        sleep(0.5)


#=-   ---===---   -=#
#

#####
#####   END   #

    log_write(f"Steps     : {Steps}\nCells was : {Cells_Was}\nCells left: {Cells_Left}"
              f"\nCells all : {Cells_Born + Cells_Was}\nCells born: {Cells_Born}\nCells died: {Cells_Died}",
              0, end_of_msg="\n\n\n", start_of_msg="\n\n", zero_log_prefix="", between_part="")

    exit()

#####=-   ---===---   -=#
#####

########
