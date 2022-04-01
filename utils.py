from PIL import Image, ImageDraw
from hold_setups import HOLD_SETUPS
import matplotlib.pyplot as plt
import numpy as np

rot_dict = {
    "N": 0,
    "NE": 45,
    "E": 90,
    "SE": 135,
    "S": 180,
    "SW": 225,
    "W": 270,
    "NW": 315,
    
}
x_coords = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
x_coord_map = {x: idx * 50 + 93 for idx,x in enumerate(x_coords)}

y_coords = [str(i) for i in range(1, 19)][::-1]
y_coord_map = {y: idx * 50 + 86 for idx,y in enumerate(y_coords)}
#
coords_map = []
for x in x_coords:
    for y in y_coords:
        coords_map.append("{}{}".format(x, y))
#
coords_map = {v: i for i, v in enumerate(coords_map)}

hold_map = {str(i):"h{}.png".format(i) for i in range(1, 202)}
hold_map_wood = {"w{:02d}".format(i): "hw{:02d}.png".format(i) for i in range(1, 81)}
hold_map.update(hold_map_wood)


def grade_maps(grade_names):
    grade_to_num = {g:i for i,g in enumerate(grade_names)}
    num_to_grade = {i:g for g,i in grade_to_num.items()}
    return grade_to_num, num_to_grade


def get_color(isStart, isEnd):
    if isStart is True:
        return "#00ff00"
    if isEnd is True:
        return "#ff0000"
    return "#0000ff"

def draw_moves(board, moves, r=30, copy=True):
    if copy is True:
        board = board.copy()    
    draw = ImageDraw.Draw(board)
    for move in moves:
        pos = move["description"]
        px = x_coord_map[pos[:1]]
        py = y_coord_map[pos[1:]]
        col = get_color(move["isStart"], move["isEnd"])
        draw.ellipse([(px-r, py-r), (px+r, py+r)], fill = None, outline =col, width=5)
    return board

def draw_coords(board, coords, r=30, copy=True):
    if copy is True:
        board = board.copy()    
    draw = ImageDraw.Draw(board)
    for coord in coords:
        px = x_coord_map[coord[:1]]
        py = y_coord_map[coord[1:]]
        col = get_color(False, False)
        draw.ellipse([(px-r, py-r), (px+r, py+r)], fill = None, outline =col, width=5)
    return board


def get_board_setup(p_board, p_holds, year):
    board = Image.open(p_board)
    for hid, hrot, hpos in HOLD_SETUPS[year]:
        p_hold = p_holds / hold_map[hid]
        assert p_hold.exists()
        img_hold = Image.open(p_hold)
        angle = rot_dict[hrot]
        img_hold = img_hold.rotate(360-angle)
        #
        px_center = x_coord_map[hpos[:1]]
        py_center = y_coord_map[hpos[1:]]
        #
        h, w = img_hold.size
        #
        px = px_center - w // 2
        py = py_center - h // 2
        #
        board.paste(img_hold, (px, py), img_hold)
    return board


def plot_mat(mat, row_names=None, col_names=None, scale_factor=2,
             title=None, xlabel=None, ylabel=None, p_file=None, vmin=None, vmax=None,
             cmap="copper", lab_format="{:.2f}"
            ):
    n_rows, n_cols = mat.shape
    fig, ax = plt.subplots(figsize=(n_cols * scale_factor,
                                    n_rows * scale_factor))
    im = ax.imshow(mat, cmap=cmap, vmin=vmin, vmax=vmax)
    #
    ax.set_xticks(np.arange(n_cols))
    ax.set_yticks(np.arange(n_rows))
    #

    if row_names is not None:
        assert len(row_names) == n_rows
        ax.set_yticklabels(row_names)
    if col_names is not None:
        assert len(col_names) == n_cols
        ax.set_xticklabels(col_names)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for col_idx in range(n_cols):
        for row_idx in range(n_rows):
            text = ax.text(col_idx, row_idx, lab_format.format(mat[row_idx, col_idx]),
                           ha="center", va="center", color="w")
    if title is not None:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    fig.tight_layout()
    if p_file is not None:
        plt.savefig(p_file)
    plt.show()

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
