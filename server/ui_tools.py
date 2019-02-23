import copy

DEFAULT_COLOR = 'rgba(200, 200, 200, 1)'

FLASH_TO_COLORS = {}
FLASH_TO_COLORS[True] = 'rgba(220, 0, 0, 0.5)'
FLASH_TO_COLORS[False] = 'rgba(255, 255, 255, 1)'

COLORS_TO_FLASH = {v: k for k, v in FLASH_TO_COLORS.items()}

WINDOW_MAX_WIDTH_TRIGGER = 600

DISPLAY_FONTSIZE_RATIO = 0.10
DISPLAY_FONTSIZE = '{}vw'.format(100 * DISPLAY_FONTSIZE_RATIO)
DISPLAY_MAXFONTSIZE = '{}px'.format(WINDOW_MAX_WIDTH_TRIGGER * DISPLAY_FONTSIZE_RATIO)

CODE_FONTSIZE_RATIO = 0.15
CODE_FONTSIZE = '{}vw'.format(100 * CODE_FONTSIZE_RATIO)
MAX_CODE_FONTSIZE = '{}px'.format(WINDOW_MAX_WIDTH_TRIGGER * CODE_FONTSIZE_RATIO)


def push_grid_to_panel(socketio, room_id, grid, panel_index):
    socketio.emit('grid', {"panel_index": panel_index, "grid": grid}, room=room_id)

def build_display_grid(n_row, n_column, flash_patterns=None):
    i_number = 0
    display_grid = []
    for i_row in range(n_row):
        display_grid.append([])
        for i_column in range(n_column):

            tile_info = {}
            tile_info['index'] = 'display_{}'.format(i_number)
            tile_info['message'] = str(i_number)

            style = {}
            style['fontSize'] = DISPLAY_FONTSIZE
            style['maxFontSize'] = DISPLAY_MAXFONTSIZE
            style['maxWidthTrigger'] = WINDOW_MAX_WIDTH_TRIGGER
            if flash_patterns is None:
                style['background'] = DEFAULT_COLOR
            else:
                style['background'] = FLASH_TO_COLORS[flash_patterns[i_number]]
            style['isBackgroundImage'] = False
            tile_info['style'] = style

            display_grid[i_row].append(tile_info)
            i_number += 1

    return display_grid


def build_code_grid(code_list, grid_layout=None):

    if grid_layout is None:
        grid_layout = [[True for _ in code_list]]  # all in one row

    i_number = 0
    code_grid = copy.deepcopy(grid_layout)
    for i, row in enumerate(grid_layout):
        for j, valid_emplacement in enumerate(row):
            tile_info = {}
            if valid_emplacement:
                tile_info['index'] = 'code_{}'.format(i_number)
                tile_info['message'] = str(code_list[i_number])

                style = {}
                style['fontSize'] = DISPLAY_FONTSIZE
                style['maxFontSize'] = DISPLAY_MAXFONTSIZE
                style['maxWidthTrigger'] = WINDOW_MAX_WIDTH_TRIGGER
                style['background'] = DEFAULT_COLOR
                style['isBackgroundImage'] = False
                tile_info['style'] = style

                code_grid[i][j] = tile_info
                i_number += 1
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

            style = {}
            style['background'] = DEFAULT_COLOR
            style['isBackgroundImage'] = False
            tile_info['style'] = style

            pad_grid[i_row].append(tile_info)
            i_number += 1
    return pad_grid


def update_grid_colors(grid, colors):
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            grid[i][j]['style']['background'] = colors[i][j]
            grid[i][j]['style']['isBackgroundImage'] = False
    return grid


def flash_patterns_from_displayed_grid(displayed_grid):

    flash_patterns = []

    for i, row in enumerate(displayed_grid):
        for j, column in enumerate(row):
            if displayed_grid[i][j]:
                if displayed_grid[i][j]['style']['isBackgroundImage']:
                    raise NotImplemented()
                else:
                    flash_value = COLORS_TO_FLASH[
                        displayed_grid[i][j]['style']['background']]
                flash_patterns.append(flash_value)

    return flash_patterns


def colors_from_index_flash_values(grid, index_to_flash_values_dict):

    # deep copy to keep same structure [i][j] but not alter content
    colors = copy.deepcopy(grid)

    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            color_value = DEFAULT_COLOR  # default to DEFAULT_COLOR
            if grid[i][j]:
                if grid[i][j]['index'] in index_to_flash_values_dict:
                    # replace with color
                    flash_value = index_to_flash_values_dict[grid[i][j]['index']]
                    color_value = FLASH_TO_COLORS[flash_value]

            colors[i][j] = color_value

    return colors
