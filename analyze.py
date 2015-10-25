#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, MultipleLocator
from gomill import sgf, sgf_moves
import group_finder

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

def directory_map(dir, fn):
    '''
    Applies fn to every file path in dir.
    Returns a list of results.

    '''
    results = []
    for root, dirs, files in os.walk(dir):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            results.append(fn(os.path.join(root, file)))

    return results

def pad_hist(counts, target_length):
    '''
    Pad *counts* with 0s so its length becomes target_length.

    '''
    new_counts = np.zeros(target_length)
    new_counts[:counts.size] = counts
    return new_counts

def examine_game():
    # Load boards at specified moves
    path = 'KGS2005/2005-01-01-5.sgf'
    counts_list, moves = load_counts(path)

    # Figure out largest number of bins
    max_binlen = max([len(counts) for counts in counts_list])
    # Pad counts
    counts_list = [pad_hist(counts, max_binlen) for counts in counts_list]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Keep track of highest group bin count
    max_counts = 0
    # Sexy colors
    cmap = plt.get_cmap('jet')
    #cmap = lambda r: (1, 0, 0, r)

    all_bins = np.arange(1, max_binlen + 1)   # the x locations for the groups
    width = 1.0 / (len(moves) + 1.0)      # the width of the bars
    rects = []

    # Plot group size histogram
    for i in range(len(moves)):
        counts = counts_list[i]
        ax.bar(all_bins + width * i - 0.5 + width / 2, counts, width, color = cmap(i / float(len(moves))), \
                label = str(moves[i]) + ' moves')

        # Keep track of largest group frequency over the set of moves
        max_counts = max(max_counts, max(counts))

    # Make the plot pretty
    ax.set_xlabel('Group sizes')
    ax.set_ylabel('Counts')
    ax.set_ylim(0.0, max_counts + 1)
    ax.set_xlim(0.5, max_binlen + 1)
    plt.legend(loc='upper right')

    # Set ticks to appear between bins and to label x positions of bins
    major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(major_locator)
    plt.tick_params(which='major', length = 0)
    minor_locator = FixedLocator(np.arange(0.5, max_binlen + 1.5, 1.0))
    ax.xaxis.set_minor_locator(minor_locator)

    # Draw the plot
    plt.show()

def load_counts(path):
    '''
    Loads the group size counts for the specified game.
    
    '''
    board, plays = load_game(path)
    moves = range(50, len(plays), 50)
    b_boards, w_boards = zip(*get_positions(board, plays, moves))

    # Check group sizes at each move
    b_bins, b_counts = zip(*[group_finder.get_group_hists(bb) for bb in b_boards])
    w_bins, w_counts = zip(*[group_finder.get_group_hists(wb) for wb in w_boards])
    bins_list, counts_list = zip(*[group_finder.combine_hists(bbs, bcs, wbs, wcs) \
            for bbs, bcs, wbs, wcs in zip(b_bins, b_counts, w_bins, w_counts)])

    return counts_list, moves

'''
def average_games():
    counts_list = directory_map('KGS2005', lambda g: load_game(
'''

##################################################

if __name__ == '__main__':
    # Histogram game lengths
    #game_lengths = directory_map("KGS2005", lambda x: len(load_game(x)[1]))
    #
    #fig = plt.figure()
    #ax = fig.add_subplot(1, 1, 1)
    #ax.hist(game_lengths, 35)
    #plt.show()

    ##############################################

    examine_game()

    #average_games()


