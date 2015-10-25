#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, MultipleLocator
import group_finder
from parse import load_game, get_positions
from util import directory_map

def examine_game():
    # Load boards at specified moves
    path = 'KGS2005/2005-01-01-5.sgf'
    counts_list, moves = load_counts(path, 50, 50)

    # Figure out largest number of bins
    max_num_groups = max([len(counts) for counts in counts_list])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Keep track of highest group bin count
    max_counts = 0
    # Sexy colors
    cmap = plt.get_cmap('jet')
    #cmap = lambda r: (1, 0, 0, r)

    width = 1.0 / (len(moves) + 1.0)      # the width of the bars

    # Plot group size histogram
    for i in range(len(moves)):
        counts = counts_list[i]
        # Can infer the correct bins by looking at the length of counts
        ax.bar(np.arange(1, len(counts) + 1) + width * i - 0.5 + width / 2, counts, width, \
                color = cmap(i / float(len(moves))), label = str(moves[i]) + ' moves')

        # Keep track of largest group frequency over the set of moves
        max_counts = max(max_counts, max(counts))

    # Make the plot pretty
    ax.set_xlabel('Group sizes')
    ax.set_ylabel('Counts')
    ax.set_ylim(0.0, max_counts + 1)
    ax.set_xlim(0.5, max_num_groups + 1)
    plt.legend(loc='upper right')

    # Set ticks to appear between bins and to label x positions of bins
    major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(major_locator)
    plt.tick_params(which='major', length = 0)
    minor_locator = FixedLocator(np.arange(0.5, max_num_groups + 1.5, 1.0))
    ax.xaxis.set_minor_locator(minor_locator)

    # Draw the plot
    plt.show()

def load_counts(path, first_check, move_step):
    '''
    Loads the group size counts for the specified game.
    
    '''
    board, plays = load_game(path)
    moves = range(first_check, len(plays), move_step)
    b_boards, w_boards = zip(*get_positions(board, plays, moves))

    # Check group sizes at each move
    b_bins, b_counts = zip(*[group_finder.get_group_hists(bb) for bb in b_boards])
    w_bins, w_counts = zip(*[group_finder.get_group_hists(wb) for wb in w_boards])
    bins_list, counts_list = zip(*[group_finder.combine_hists(bbs, bcs, wbs, wcs) \
            for bbs, bcs, wbs, wcs in zip(b_bins, b_counts, w_bins, w_counts)])

    return counts_list, moves

def average_games():
    # Get counts for each game in the directory
    counts_list_list = directory_map('KGS2005', lambda p: load_counts(p, 50, 50)[0])

    max_binlen = max([len(counts) for counts in counts_list_list])

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


