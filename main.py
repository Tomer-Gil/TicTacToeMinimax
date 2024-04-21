import numpy as np

N = 3
X_WIN_SCORE = 1
TIE_SCORE = 0
O_WIN_SCORE = -1


def is_win(board, is_x):
    """

    :param board:
    :param is_x: True if it's X turn, False otherwise
    :return:
    """
    is_x = 1 if is_x else -1
    # Check rows
    for i in range(N):
        if board[i].sum() == N * is_x:
            return True
    # Check columns
    for i in range(N):
        if board[:, i].sum() == N * is_x:
            return True
    # Check diagonals
    if board.diagonal().sum() == N * is_x or np.fliplr(board).diagonal().sum() == N * is_x:
        return True
    return False


def is_x_wins(board):
    return is_win(board, is_x=True)


def is_o_wins(board):
    return is_win(board, is_x=False)


def is_terminal_node(board):
    return not (board == 0).sum()  # iff (board == 0).sum() == 0


def get_score(board):
    """Heuristic function"""
    # TODO: rewrite this comment
    # If board is full, score is 0 (we assume that the minute someone won, the game stops, so if we got a
    if is_x_wins(board):
        return X_WIN_SCORE
    if is_o_wins(board):
        return O_WIN_SCORE
    return TIE_SCORE


def minimax(board, depth, is_maximizer):
    """

    :param board: a node in the tree
    :param depth: depth in the recursion tree
    :param is_maximizer:
    :return:
    """
    # if is_x_wins(board) or is_o_wins(board) or is_terminal_node(board):
    #     return get_score(board)
    if is_x_wins(board) or is_o_wins(board) or depth == 0 or is_terminal_node(board):
        return get_score(board)
    if is_maximizer:
        best_value = -np.inf
        for row, col in np.argwhere(board == 0):
            board[row, col] = 1
            val = minimax(board, depth - 1, False)
            best_value = max(best_value, val)
            board[row, col] = 0
        return best_value
    # else
    best_value = np.inf
    for row, col in np.argwhere(board == 0):
        board[row, col] = -1
        val = minimax(board, depth - 1, True)
        best_value = min(best_value, val)
        board[row, col] = 0
    return best_value


def play_ai_turn(board, depth):
    best_value = -np.inf
    best_row, best_col = -1, -1
    for row, col in np.argwhere(board == 0):
        board[row, col] = 1
        val = minimax(board, depth - 1, False)
        if val > best_value:
            best_row, best_col = row, col
        best_value = max(best_value, val)
        board[row, col] = 0
    board[best_row, best_col] = 1


def play_human_turn(board):
    print(board)
    print("Enter row, col for this board: ", sep="")
    row, col = int(input()), int(input())
    board[row, col] = -1


def play_game(board):
    is_game_ended = False
    i = 0
    depth = N * N  # Usually 9
    while not is_game_ended:
        if i % 2 == 0:
            play_ai_turn(board, depth)
        else:
            play_human_turn(board)
        depth -= 1
        if depth == 0:
            is_game_ended = True
        i += 1
    print(board)


if __name__ == "__main__":
    board = np.zeros((N, N))
    play_game(board)
