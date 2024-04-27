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


def cancel_piece(board, row, col):
    board[row][col] = 0

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


def get_input(player, board):
    sign = getsign(player)
    pos = input(sign + ", your turn : ")
    while not turn(pos, player, board)[0]:
        pos = input(sign + ", your turn : ")


def turn(column, player, board):
    """
    returns a tuple, the first value is if the action is valid, the second is whether the player has won
    the column arg is a string and might be wrong, if it is return False
    """
    nb_cols = len(board[0])
    nb_rows = len(board)
    if not column.isdigit() or int(column) > nb_cols or int(column) < 1:
        return (False, False)
    int_col = int(column) - 1
    if board[nb_rows - 1][int_col] != 0 or player != 1 and player != 2:
        return (False, False)
    drop_piece(board, get_next_open_row(board, int_col), int_col, player)
    return (True, winning_move(board, player))


def play(w, h):
    board = init_board(w, h, 0)
    print()
    print(" - - - PUISSANCE 4 - - - ")
    print()
    print("Player 1 " + '\033[91m' + "██" + '\033[0m')
    diff1 = 1
    diff2 = 1
    p1 = input("[1]Human [2]Ai :")
    while not p1.isdigit() or int(p1) > 2 or int(p1) < 1:
        p1 = input(": ")
    if p1 == "2":
        diff1 = choose_difficulty()
    print()
    print("Player 2 " + '\033[93m' + "██" + '\033[0m')
    p2 = input("[1]Human [2]Ai :")
    while not p2.isdigit() or int(p2) > 2 or int(p2) < 1:
        p2 = input(": ")
    if p2 == "2":
        diff2 = choose_difficulty()
    playing = 1
    coup = 0
    while coup < w * h and not winning_move(board, 1) and not winning_move(board, 2):
        print_board(board)
        print("p1 heuristic :",heuristic(board,1))
        start_time = time.time()
        if playing == 1:
            get_input(1, board) if p1 == "1" else ai_input(1, board, diff1)
        else:
            get_input(2, board) if p2 == "1" else ai_input(2, board, diff2)
            
        end_time = time.time()
        execution_time = round(end_time - start_time,2)

        print("Time taken:", execution_time, "seconds")

        playing = playing % 2 + 1
        coup += 1
    if coup >= w * h:
        print_board(board)
        print("It's a draw !")
    else:
        print_board(board)
        sign = getsign(playing % 2 + 1)
        print(sign + " has won the game !")


def choose_difficulty():
    print()
    print("Choose your level of difficulty :")
    print("1 : Random")
    print("2 : Greedy")
    print("3 : Minimax depth 3")
    print("4 : Minimax depth 6")
    diff = input(": ")
    while not diff.isdigit() or int(diff) > 4 or int(diff) < 1:
        diff = input(": ")
    diff = int(diff)
    return diff


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

def local_evaluation(local_row, player):
    other = player % 2 + 1
    if local_row.count(player) == 4:
        return 1000
    elif local_row.count(player) == 3 and local_row.count(0) == 1:
        return 5
    elif local_row.count(player) == 2 and local_row.count(0) == 2:
        return 2
    elif local_row.count(other) == 3 and local_row.count(0) == 1:
        return -5
    elif local_row.count(other) == 2 and local_row.count(0) == 2:
        return -2
    elif local_row.count(other) == 4:
        return -1000
    else:
        return 0


def heuristic(board, player):
    score = 0
    WINDOW_LENGTH = 4
    nb_col = len(board[0])
    nb_row = len(board)

    ## Score center column
    center_array = []
    for i in range(nb_row):
        center_array.append(board[i][nb_col // 2])
    center_count = center_array.count(player)
    score += center_count * 3

    ## Score Horizontal
    for r in range(nb_row):
        row_array = board[r].copy()
        for c in range(nb_col - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += local_evaluation(window, player)

    ## Score Vertical
    for c in range(nb_col):
        col_array = []
        for i in range(nb_row):
            col_array.append(board[i][c])
        for r in range(nb_row - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += local_evaluation(window, player)

    ## Score positive sloped diagonal
    for r in range(nb_row - 3):
        for c in range(nb_col - 3):
            window = []
            for i in range(WINDOW_LENGTH):
                window.append(board[r + i][c + i])
            score += local_evaluation(window, player)

    ## Score negatively sloped diagonal
    for r in range(nb_row - 3):
        for c in range(nb_col - 3):
            window = []
            for i in range(WINDOW_LENGTH):
                window.append(board[r + 3 - i][c + i])
            score += local_evaluation(window, player)

    return score


def ai_input(player,board,diff):
    col = 0
    if diff == 1:
         col = ai_random(player,board)
    elif diff == 2:
        col = ai_greedy(player,board)
    elif diff == 3:
        col = ai_negamax(board,3,player)
    elif diff == 4:
        col = ai_negamax(board,6,player)
    else:
        raise Exception("Unknown ia")
    drop_piece(board, get_next_open_row(board, col), col, player)
    return (True, winning_move(board, player))

def ai_random(player,board):
    l = get_valid_locations(board)
    n = len(l)
    return l[random.randint(0, n-1)]

def ai_greedy(player,board):
    copy = board_copy(board)
    l = get_valid_locations(board)
    n = len(l)
    best_col = l[0]
    best_h = -9999
    # print("greedy analysis")
    for col in l:
        row = get_next_open_row(copy,col);
        drop_piece(copy, row, col,player)
        h = heuristic(copy,player)
        # print("col",col,"=",h)
        if h > best_h:
            best_h = h
            best_col = col
        cancel_piece(copy,row,col)

    return best_col

def is_terminal(board,h):
    return len(get_valid_locations(board)) == 0 or abs(h) > 900

def generate_childs(board,player):
    l = []
    v = get_valid_locations(board)
    for col in v:
        copy = board_copy(board)
        drop_piece(copy, get_next_open_row(copy, col), col, player)
        l.append((copy,col))
    return l

def ai_negamax(board,depth,player):
    other = player % 2 + 1
    max_score = -9999
    col = -1
    for child in generate_childs(board,player):
        score = -_negamax(child[0],depth-1,other,-99999,99999)
        if score > max_score:
            max_score = score
            col = child[1]
    return col

def _negamax(board,depth,player,alpha,beta): 
    h = heuristic(board,player)
    other = player % 2 + 1
    # check if terminal node
    if depth == 0 or is_terminal(board,h):
        return h
    
    max_score = -99999
    for child in generate_childs(board,player):
        score = -_negamax(child[0],depth-1,other,-beta,-alpha)
        max_score = max(max_score,score)
        alpha = max(alpha, score)
        if alpha >= beta:
            break 
    return max_score


