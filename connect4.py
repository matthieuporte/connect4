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
        firstLine += str(i + 1) + "    "
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
        sign = '\033[93m' + "██" + '\033[0m'
    elif p == 1:
        sign = '\033[91m' + "██" + '\033[0m'
    return sign


def getsign3(p):
    sign = "  "
    if p == 2:
        sign = '\033[93m' + "██" + '\033[0m'
    elif p == 1:
        sign = '\033[91m' + "██" + '\033[0m'
    elif p == 3:
        sign = '\033[94m' + "██" + '\033[0m'
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
    if M[nb_rows - 1][int_col] != 0 or player != 1 and player != 2:
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
        sign = getsign3(playing % 3 + 1)
        print(sign + " à gagné la partie !")

def play(w, h):
    T = init_board(w, h, 0)
    print()
    print(" - - - PUISSANCE 4 - - - ")
    print()
    print("Joueur 1 " + '\033[91m' + "██" + '\033[0m')
    diff1 = 1
    diff2 = 1
    j1 = input("[1]Humain [2]IA :")
    while not j1.isdigit() or int(j1) > 2 or int(j1) < 1:
        j1 = input(": ")
    if j1 == "2":
        diff1 = choose_difficulty()
    print()
    print("Joueur 2 " + '\033[93m' + "██" + '\033[0m')
    j2 = input("[1]Humain [2]IA :")
    while not j2.isdigit() or int(j2) > 2 or int(j2) < 1:
        j2 = input(": ")
    if j2 == "2":
        diff2 = choose_difficulty()
    playing = 1
    coup = 0
    while coup < w * h and not winning_move(T, 1) and not winning_move(T, 2):
        print_board(T)
        if playing == 1:
            get_input(1, T) if j1 == "1" else ia_input(1, T, diff1)
        else:
            get_input(2, T) if j2 == "1" else ia_input(2, T, diff2)
        playing = playing % 2 + 1
        coup += 1
    if coup >= w * h:
        print_board(T)
        print("égalité !")
    else:
        print_board(T)
        sign = getsign(playing % 2 + 1)
        print(sign + " à gagné la partie !")


def choose_difficulty():
    print("1 : IA Débutant")  # 1
    print("2 : IA Facile")  # 3
    print("3 : IA Moyenne")  # 5
    print("4 : IA Difficile")  # 7
    print("5 : IA Impossible")  # 9
    diff = input(": ")
    while not diff.isdigit() or int(diff) > 5 or int(diff) < 1:
        diff = input(": ")
    diff = int(diff)
    diff *= 2
    if diff == 3:
        diff -= 1
    return diff - 1 


def board_copy(board):
    h = len(board)
    w = len(board[0])
    copy = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append(board[i][j])
        copy.append(row)
    return copy


### IA FROM NOW ON ###


def ia_input(ia, M, depth):
    col = minmax(M, depth, -math.inf, math.inf, True, ia)[0]
    time.sleep(0.25)
    drop_piece(M, get_next_open_row(M, col), col, ia)


def local_evaluation(local_row, player):
    if local_row.count(player) == 4:
        return 100
    elif local_row.count(player) == 3 and local_row.count(0) == 1:
        return 5
    elif local_row.count(player) == 2 and local_row.count(0) == 2:
        return 2
    if local_row.count(player % 2 + 1) == 3 and local_row.count(0) == 1:
        return 4

    return 0


def evaluation(board, piece):
    score = 0
    WINDOW_LENGTH = 4
    nb_col = len(board[0])
    nb_row = len(board)

    ## Score center column
    center_array = []
    for i in range(nb_row):
        center_array.append(board[i][nb_col // 2])
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(nb_row):
        row_array = board[r].copy()
        for c in range(nb_col - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += local_evaluation(window, piece)

    ## Score Vertical
    for c in range(nb_col):
        col_array = []
        for i in range(nb_row):
            col_array.append(board[i][c])
        for r in range(nb_row - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += local_evaluation(window, piece)

    ## Score positive sloped diagonal
    for r in range(nb_row - 3):
        for c in range(nb_col - 3):
            window = []
            for i in range(WINDOW_LENGTH):
                window.append(board[r + i][c + i])
            score += local_evaluation(window, piece)

    for r in range(nb_row - 3):
        for c in range(nb_col - 3):
            window = []
            for i in range(WINDOW_LENGTH):
                window.append(board[r + 3 - i][c + i])
            score += local_evaluation(window, piece)

    return score


### IA ###
def minmax(board, depth, alpha, beta, isMaximizing, ia):
    '''
    :return: a tuple with the column to play and it's value
    '''
    valid_locations = get_valid_locations(board)
    if len(valid_locations) == 0: # it's a draw :(
        return None, 0
    if winning_move(board, ia):
        return None, 1000000 * depth
    if winning_move(board, ia % 2 + 1):
        return None, -13000000 * depth
    if depth == 0:
        return None, evaluation(board, ia)
    
    if isMaximizing:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            copy_of_the_board = board_copy(board)
            drop_piece(copy_of_the_board, row, col, ia)
            new_score = minmax(copy_of_the_board, depth - 1, alpha, beta, False, ia)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # is minimizing
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            copy_of_the_board = board_copy(board)
            drop_piece(copy_of_the_board, row, col, ia % 2 + 1)
            new_score = minmax(copy_of_the_board, depth - 1, alpha, beta, True, ia)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


"""
1 - get valid locations DONE
2 - check if it's the end of the board or max depth
2.1 - to check whether it is the end of the board you need to the function winning_move that tells
you if someone has one : go over the whole board (again) and check is there is a 4 e connection.
It is the end of the board if either a player has won OR if the board is full
3 - if it is the case return the value of the present board
4 - if it is not then we get real with minmax
4.1 - set the value to the lowest/highest (depending whether it is the maximising player or not)
4.2 - for every playable column make a copy, drop a piece and call minmax with this board copied
4.3 - once the recursion is done we store the value in a variable, if it is bigger/smaller that the value 
we already had set then we can modify it, and the column as well
4.4 - we can also do an alpha beta optimisation, beta is set with the minimiser, it starts at +infinity 
and then is set to the minimal value between the min value found when calling the minimiser and it's value
The same is done with alpha (except that it starts at -infinity and we take the max)
Now if at any time alpha>=beta you can stop searching here, the value will not be interesting
If you want to get a better understanding this website is great :
https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
"""
