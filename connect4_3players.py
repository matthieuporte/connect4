import random
import math
import time


def init_board(w, h, val):
    """
    return a new l x c matrix full of val
    """
    M = []
    for i in range(h):
        M.append([])
        for j in range(w):
            M[i].append(val)
    return M


def print_board(M):
    l = len(M)
    c = len(M[0])
    firstLine = "  "
    print()
    for i in range(c):
        print("%4s "%str(i + 1),end='')
        #firstLine += str(i + 1) + "    "
    print(firstLine)
    print("┌" + "────┬" * (c - 1) + "────┐")
    for i in range(l - 1):
        line = "│"
        for j in range(c):
            line += " " + getsign(M[l - i - 1][j]) + " │"
        print(line)
        print("├" + "────┼" * (c - 1) + "────┤")
    line = "│"
    for j in range(c):
        line += " " + getsign(M[0][j]) + " │"
    print(line)
    print("└" + "────┴" * (c - 1) + "────┘")


# ┼ ┴ ┤┬ ├ ┘└ ┐┌ ─ │

def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[len(board) - 1][col] == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(len(board[0])):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def get_next_open_row(board, col):
    for r in range(len(board)):
        if board[r][col] == 0:
            return r

def getsign(p):
    sign = "  "
    if p == 2:
        sign = '\033[94m' + "██" + '\033[0m'
    elif p == 1:
        sign = '\033[91m' + "██" + '\033[0m'
    elif p == 3:
        sign = '\033[92m' + "██" + '\033[0m'
    return sign


def is_terminal_node(board):
    return len(get_valid_locations(board)) == 0 or winning_move(board, 1) or winning_move(board, 2)


def winning_move(board, player):
    nb_col = len(board[0])
    nb_row = len(board)
    # Check horizontal locations for win
    for c in range(nb_col - 3):
        for r in range(nb_row):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and \
                    board[r][c + 3] == player:
                return True

    # Check vertical locations for win
    for c in range(nb_col):
        for r in range(nb_row - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and \
                    board[r + 3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(nb_col - 3):
        for r in range(nb_row - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and \
                    board[r + 3][c + 3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(nb_col - 3):
        for r in range(3, nb_row):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and \
                    board[r - 3][c + 3] == player:
                return True
    return False


def get_input(player, M):
    sign = getsign(player)
    pos = input(sign + ", à vous de jouer : ")
    while not turn(pos, player, M)[0]:
        pos = input(sign + ", à vous de jouer : ")


def turn(column, player, M):
    """
    returns a tuple, the first value is if the action is valid, the second is whether the player has won
    the column arg is a string and might be wrong, if it is return False
    """
    nb_cols = len(M[0])
    nb_rows = len(M)
    if not column.isdigit() or int(column) > nb_cols or int(column) < 1:
        return (False, False)
    int_col = int(column) - 1
    if M[nb_rows - 1][int_col] != 0 or player != 1 and player != 2 and player != 3:
        return (False, False)
    drop_piece(M, get_next_open_row(M, int_col), int_col, player)
    return (True, winning_move(M, player))


def play3(w,h):
    T = init_board(w, h, 0)
    print()
    print(" - - - PUISSANCE 4 | 3 Joueurs - - - ")
    print()
    playing = 1
    coup = 0
    while coup < w * h and not winning_move(T, 1) and not winning_move(T, 2):
        print_board(T)
        get_input(playing,T)
        playing = playing % 3 + 1
        coup += 1
    if coup >= w * h:
        print_board(T)
        print("égalité !")
    else:
        print_board(T)
        sign = getsign((playing - 1)% 3)
        print(sign + " à gagné la partie !")