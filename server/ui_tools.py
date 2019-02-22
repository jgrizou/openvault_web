import copy

FLASH_TO_COLORS = {}
FLASH_TO_COLORS[True] = 'rgba(220, 0, 0, 0.5)'
FLASH_TO_COLORS[False] = 'rgba(255, 255, 255, 1)'

COLORS_TO_FLASH = {v: k for k, v in FLASH_TO_COLORS.items()}

DISPLAY_FONTSIZE = "50px"
CODE_FONTSIZE = "100px"



def push_grid_to_panel(socketio, room_id, grid, panel_index):
    socketio.emit('grid', {"panel_index": panel_index, "grid": grid}, room=room_id)

def push_colors_to_panel(socketio, room_id, colors, panel_index):
    socketio.emit('colors', {"panel_index": panel_index, "colors": colors}, room=room_id)


def build_display_grid(n_row, n_column, indexes=None, fontSize=DISPLAY_FONTSIZE):
    i_number = 0
    display_grid = []
    for i_row in range(n_row):
        display_grid.append([])
        for i_column in range(n_column):

            tile_info = {}
            if indexes is not None:
                tile_info['index'] = indexes[i_row][i_column]
            else:
                tile_info['index'] = 'display_{}'.format(i_number)
            tile_info['message'] = str(i_number)
            tile_info['fontSize'] = fontSize

            display_grid[i_row].append(tile_info)
            i_number += 1

    return display_grid


def build_code_grid(code_list, indexes=None, fontSize=CODE_FONTSIZE):
    code_row = []
    for i_number, number in enumerate(code_list):
        tile_info = {}
        if indexes is not None:
            tile_info['index'] = indexes[i_number]
        else:
            tile_info['index'] = 'code_{}'.format(i_number)
        tile_info['message'] = str(number)
        tile_info['fontSize'] = fontSize
        code_row.append(tile_info)
    code_grid = [code_row]
    return code_grid


def build_pad_grid(n_row, n_column, indexes=None):
    i_number = 0
    pad_grid = []
    for i_row in range(n_row):
        pad_grid.append([])
        for i_column in range(n_column):
            tile_info = {}
            if indexes is not None:
                tile_info['index'] = indexes[i_row][i_column]
            else:
                tile_info['index'] = 'pad_{}'.format(i_number)
            pad_grid[i_row].append(tile_info)
            i_number += 1
    return pad_grid


def display_colors_from_flash_patterns(display_grid, flash_patterns, flash_to_colors=FLASH_TO_COLORS):

    # deep copy to keep same structure [i][j] but not alter content
    display_colors = copy.deepcopy(display_grid)

    flash_index = 0
    for i, row in enumerate(display_grid):
        for j, column in enumerate(row):
            if display_grid[i][j]:
                # replace with color
                display_colors[i][j] = flash_to_colors[flash_patterns[flash_index]]
                flash_index += 1
            else:
                display_colors[i][j] = '' # erase the copy

    return display_colors


def flash_patterns_from_display_colors(display_colors, colors_to_flash=COLORS_TO_FLASH):

    flash_patterns = []

    for i, row in enumerate(display_colors):
        for j, column in enumerate(row):
            if display_colors[i][j]:
                flash_value = colors_to_flash[display_colors[i][j]]
                flash_patterns.append(flash_value)

    return flash_patterns
