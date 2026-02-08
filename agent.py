"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions from othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {} # Use this for state caching

def eprint(*args, **kwargs): #use this for debugging, to print to sterr
    print(*args, file=sys.stderr, **kwargs)
    
def compute_utility(board, color):
    # IMPLEMENT!
    """
    Method to compute the utility value of board.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents utility
    """
    dark_score, light_score = get_score(board)

    if color == 1:
        return dark_score - light_score
    else:
        return light_score - dark_score

def compute_heuristic(board, color):
    # IMPLEMENT! 
    """
    Method to heuristic value of board, to be used if we are at a depth limit.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents heuristic value
    """
    # My heuristic takes the weighted sum of each of the following factors: 
    # 1. Piece Difference
    # 2. Number of possible moves
    # 3. Difference in Corners Captured
    # 4. Difference in Edges Captured

    # Piece Difference
    opponent = 3 - color
    my_count, opponent_count = get_score(board)

    if color == 1:
        piece_diff = my_count - opponent_count
    else:
        piece_diff = opponent_count - my_count
    
    # Number of Possible Moves
    my_moves = len(get_possible_moves(board, color))
    opponent_moves = len(get_possible_moves(board, opponent))
    possible_moves = my_moves - opponent_moves

    # Corners Captured
    corners = [(0, 0), (0, len(board) - 1), (len(board) - 1, 0), (len(board) - 1, len(board) - 1)]
    my_corners = sum([1 for corner in corners if board[corner[0]][corner[1]] == color])
    opponent_corners = sum([1 for corner in corners if board[corner[0]][corner[1]] == opponent])
    corner_score = my_corners - opponent_corners

    # # Edges Captured
    # edges = [(0, i) for i in range(len(board))] + [(i, 0) for i in range(len(board))] + [(len(board) - 1, i) for i in range(len(board))] + [(i, len(board) - 1) for i in range(len(board))]
    # my_edges = sum([1 for edge in edges if board[edge[0]][edge[1]] == color])
    # opponent_edges = sum([1 for edge in edges if board[edge[0]][edge[1]] == opponent])
    # edge_score = my_edges - opponent_edges

    return 10 * piece_diff + 3 * possible_moves + 20 * corner_score # + 5 * edge_score


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the lowest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the max utiltiy
    # 4. After checking every move, you can find the minimum utility
    # ...

    if caching and board in cache:
        cache_utility = cache[board]
        return None, cache_utility
    
    allowed_moves = get_possible_moves(board, 3 - color)

    # Check if currently at the terminal state
    if not allowed_moves or limit == 0:
        return None, compute_utility(board, color)

    best_move = None
    min_utility = float('inf')

    # For each possible move, get the max utility, and find the overall minimum utility
    for move in allowed_moves:

        new_board = play_move(board, 3 - color, move[0], move[1])
        _, utility = minimax_max_node(new_board, color, limit - 1, caching)

        if utility < min_utility:
            best_move = move
            min_utility = utility

    # Store the board in cache to improve efficiency
    if caching:
        cache[board] = min_utility

    return best_move, min_utility

def minimax_max_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the highest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the min utiltiy
    # 4. After checking every move, you can find the maximum utility
    # ...
    
    if caching and board in cache:
        cache_utility = cache[board]
        return None, cache_utility
    
    allowed_moves = get_possible_moves(board, color)

    # Check if currently at the terminal state
    if not allowed_moves or limit == 0:
        return None, compute_utility(board, color)
    
    best_move = None
    max_utility = float('-inf')

    # For each possible move, get the min utility, and find the overall maximum utility
    for move in allowed_moves:
        new_board = play_move(board, color, move[0], move[1])
        _, utility = minimax_min_node(new_board, color, limit - 1, caching)

        if utility > max_utility:
            best_move = move
            max_utility = utility
    
    # Store the board in cache to improve efficiency
    if caching:
        cache[board] = max_utility
    
    return best_move, max_utility

    
def select_move_minimax(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Minimax algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a flag determining whether state caching is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    
    allowed_moves = get_possible_moves(board, color)

    # Check if currently at the terminal state
    if not allowed_moves:
        return None

    best_move = None
    max_utility = float('-inf')

    # Loop through possible moves
    for move in allowed_moves:
        new_board = play_move(board, color, move[0], move[1])
        _, utility  = minimax_min_node(new_board, color, limit - 1, caching)
    
        if utility > max_utility:
            best_move = move
            max_utility = utility

    return best_move


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the lowest possible utility (don't forget to utilize and update alpha and beta!)
    """

    if caching and board in cache:
        cache_utility = cache[board]
        return None, cache_utility

    allowed_moves = get_possible_moves(board, 3 - color)

    # Check if currently at the terminal state
    if not allowed_moves or limit == 0:
        return None, compute_utility(board, color)
    
    best_move = None
    min_utility = float('inf')

    # If ordering is enabled, sort the allowed moves based on the utility value, where the lower the value, the better
    if ordering:
        allowed_moves.sort(key=lambda move: compute_utility(play_move(board, 3 - color, move[0], move[1]), color))
    
    # For each possible move, get the max utility, and find the overall minimum utility
    for move in allowed_moves:
        new_board = play_move(board, 3- color, move[0], move[1])
        _, utility = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)

        if utility < min_utility:
            best_move = move
            min_utility = utility

        # Perform alpha-beta pruning, update beta
        beta = min(beta, min_utility)
        if beta <= alpha:
            # If beta is less than alpha, then prune the remaining moves/branches
            break
    
    # Store the board in cache to improve efficiency
    if caching:
        cache[board] = min_utility

    return best_move, min_utility


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the highest possible utility (don't forget to utilize and update alpha and beta!)
    """

    if caching and board in cache:
        cache_utility = cache[board]
        return None, cache_utility
    
    allowed_moves = get_possible_moves(board, color)

    # Check if currently at the terminal state
    if not allowed_moves or limit == 0:
        return None, compute_utility(board, color)
    
    best_move = None
    max_utility = float('-inf')

    # If ordering is enabled, sort the allowed moves based on the utility value, where the higher the value, the better
    if ordering:
        allowed_moves.sort(key=lambda move: compute_utility(play_move(board, color, move[0], move[1]), color), reverse=True)

    # For each possible move, get the min utility, and find the overall maximum utility
    for move in allowed_moves:
        new_board = play_move(board, color, move[0], move[1])
        _, utility = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)

        if utility > max_utility:
            best_move = move
            max_utility = utility

        # Perform alpha-beta pruning, update alpha
        alpha = max(alpha, max_utility)
        if beta <= alpha:
            # If beta is less than alpha, then prune the remaining moves/branches
            break
    
    # Store the board in cache to improve efficiency
    if caching:
        cache[board] = max_utility

    return best_move, max_utility

def select_move_alphabeta(board, color, limit = -1, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Alpha-Beta algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    INPUT: a game state, the player that is in control, the depth limit for the search, a flag determining whether state caching is on or not, a flag determining whether node ordering is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """


    # best_move, _ = alphabeta_max_node(board, color, float('-inf'), float('inf'), limit, caching, ordering)
    # return best_move
    
    allowed_moves = get_possible_moves(board, color)

    # Check if currently at the terminal state
    if not allowed_moves:
        return None
    
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    
    # If ordering is enabled, sort the allowed moves based on the utility value, where the higher the value, the better
    if ordering:
        allowed_moves.sort(key=lambda move: compute_utility(play_move(board, color, move[0], move[1]), color), reverse=True)

    # For each possible move, get the min utility, and find the overall maximum utility
    for move in allowed_moves:
        new_board = play_move(board, color, move[0], move[1])
        _, utility = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)

        if utility > alpha:
            best_move = move
            alpha = utility

    return best_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) # Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) # Depth limit
    minimax = int(arguments[2]) # Minimax or alpha beta
    caching = int(arguments[3]) # Caching 
    ordering = int(arguments[4]) # Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
