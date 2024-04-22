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
    # The last condition - iff (board == 0).sum() == 0
    return is_x_wins(board) or is_o_wins(board) or not (board == 0).sum()


def get_score(board):
    """Heuristic function"""
    # TODO: rewrite this comment
    # If board is full, score is 0 (we assume that the minute someone won, the game stops, so if we got a
    if is_x_wins(board):
        return X_WIN_SCORE
    if is_o_wins(board):
        return O_WIN_SCORE
    return TIE_SCORE


def minimax(board, depth, alpha, beta, is_maximizer):
    """
    Minimax algorithm, using alpha-beta pruning.

    In a maximizer turn, alpha holds a lower bound on the score the maximizer will return, i.e., the number the
    maximizer will return will be at least alpha.

    Analogously, in a minimizer turn, beta holds an upper bound on the score the minimizer will return, i.e., the
    number the minimizer will return will be at most beta.

    Alpha and beta are passed together, so, the meaning of beta in a maximizer turn is an upper bound on the score its
    father (predecessor) will return. Or simply, it means that it's father will return something which is at most beta.

    So, if it's the maximizer turn, and alpha is greater than beta, than the maximizer can give up his turn and just
    return the score of alpha, because anyway, it will only return something which is greater than/equals to alpha,
    which we assume now is greater than beta, and it's father won't choose it.
    For example, if it's the (the beginning of the) maximizer turn, and alpha = inf, beta = 3, and after a certain
    move alpha becomes 5. So it means that the maximizer will return 5 or above to it's father.
    But it's father is a minimizer, and will pick something which is at most 3, and so the its redundant for the
    maximizer to keep test the rest of it's moves.

    # TODO: Add analogous explanation for the minimizer turn.
    :param board: a node in the tree
    :param depth: depth in the recursion tree
    :param is_maximizer:
    :return:
    """
    if depth == 0 or is_terminal_node(board):
        return get_score(board), None, None

    # Save the optimal move
    best_row, best_col = -1, -1

    if is_maximizer:
        best_value = -np.inf
        for row, col in np.argwhere(board == 0):
            board[row, col] = 1
            val, *_ = minimax(board, depth - 1, alpha, beta, False)

            # Save the optimal move
            if val > best_value:
                best_row, best_col = row, col

            best_value = alpha = max(best_value, val)
            board[row, col] = 0

            # Alpha-beta pruning
            if alpha >= beta:
                break
        return best_value, best_row, best_col
    # else
    best_value = np.inf
    for row, col in np.argwhere(board == 0):
        board[row, col] = -1
        val, *_ = minimax(board, depth - 1, alpha, beta, True)

        # Save the optimal move
        if val < best_value:
            best_row, best_col = row, col

        best_value = beta = min(best_value, val)
        board[row, col] = 0

        # Alpha-beta pruning
        if alpha >= beta:
            break
    return best_value, best_row, best_col


def play_ai_turn(board, depth):
    _, best_row, best_col = minimax(board, depth - 1, -np.inf, np.inf, True)
    board[best_row, best_col] = 1


def play_human_turn(board):
    print(board)
    print("Enter row, col for this board: ", sep="")
    row, col = int(input()), int(input())
    board[row, col] = -1


def play_game(board):
    is_game_ended = is_terminal_node(board)
    i = 0
    # depth = N * N  # Usually 9
    while not is_game_ended:
        if i % 2 == 0:
            play_ai_turn(board, np.inf)
        else:
            play_human_turn(board)
        is_game_ended = is_terminal_node(board)
        i += 1
    print(board)


if __name__ == "__main__":
    board = np.zeros((N, N))
    play_game(board)
