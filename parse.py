import numpy as np
from gomill import sgf, sgf_moves

def load_game(sgf_path):
    with open(sgf_path, "r") as myfile:
        content = myfile.read()

    try:
        my_game = sgf.Sgf_game.from_string(content)
    except ValueError:
        raise StandardError("bad sgf file")

    try:
        board, plays = sgf_moves.get_setup_and_moves(my_game)
    except ValueError, e:
        raise StandardError(str(e))

    return board, plays

def get_positions(board, plays, move_numbers):
    '''
    Given a gomill board, a list of plays, and a list of move numbers,
    returns a list of tuples of board configurations at the
    specified move_numbers.

    E.g. returns [(b1, w1), (b2, w2), ...], where b# and w#
    are 19x19 numpy arrays with 1s where the black and white
    pieces are respectively.

    '''
    # aggregate board positions to this list
    positions = []
    # only iterate through plays up to
    # the last move we're interested in
    last_move = np.amax(move_numbers)
    relevant_plays = plays[:last_move+1]
    for move_number, play in enumerate(relevant_plays):
        colour, move = play
        # only make a move if it's not a pass
        if move is not None:
            row, col = move
            try:
                board.play(row, col, colour)
            except ValueError:
                raise StandardError("illegal move in sgf file")

        # if we've reached a move we're interested in,
        # save the current board position
        if move_number in move_numbers:
            positions.append(board_to_numpy_arrays(board))

    return positions

def board_to_numpy_arrays(board):
    '''
    Given a 19x19 gomill board, returns a tuple of 19x19 numpy 
    arrays with 1s where the black and white pieces are respectively.

    '''
    points = board.list_occupied_points()
    plays_white = [ point[1] for point in points if point[0] is 'w' ]
    plays_black = [ point[1] for point in points if point[0] is 'b' ]
    position_black = plays_to_numpy_array(plays_black)
    position_white = plays_to_numpy_array(plays_white)
    return position_black, position_white

def plays_to_numpy_array(points):
    '''
    Given a list of points, returns a 19x19 numpy array
    with 1s at all the points and 0s everywhere else.

    '''
    coords = zip(*points)
    board_array = np.zeros([19, 19])
    board_array[coords] = 1
    return board_array
