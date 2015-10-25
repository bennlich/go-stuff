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
    print "parsing %s" % path
    board, plays = load_game(path)
    moves = range(first_check, len(plays), move_step)

    if len(moves) is 0:
        print "UhOh-- %s has %s plays" % (path, len(plays))
        return [np.zeros(1)], []

    b_boards, w_boards = zip(*get_positions(board, plays, moves))

    # Check group sizes at each move
    b_bins, b_counts = zip(*[group_finder.get_group_hists(bb) for bb in b_boards])
    w_bins, w_counts = zip(*[group_finder.get_group_hists(wb) for wb in w_boards])
    bins_list, counts_list = zip(*[group_finder.combine_hists(bbs, bcs, wbs, wcs) \
            for bbs, bcs, wbs, wcs in zip(b_bins, b_counts, w_bins, w_counts)])

    return counts_list, moves

def average_games():
    # Get counts for each game in the directory
    first_sample = 20
    move_step = 50
    # TODO: change load_counts to take list of samples!!!
    counts_list_list = directory_map('KGS2005', lambda p: load_counts(p, first_sample, move_step)[0])

    # Figure out largest group size for all checked moves in all games
    max_num_groups = max([len(counts) for counts_list in counts_list_list for counts in counts_list])
    max_num_samples = max([len(counts_list) for counts_list in counts_list_list])
    num_games = len(counts_list_list)

    # Create 3D array of all counts
    all_counts = np.zeros([num_games, max_num_samples, max_num_groups])

    for game_num, counts_list in enumerate(counts_list_list):
        for sample_num, counts in enumerate(counts_list):
            all_counts[game_num, sample_num, :counts.size] = counts

    # Average group counts
    average_over_games = np.mean(all_counts, 0)
    error_over_games = np.std(all_counts, 0) / np.sqrt(num_games)

    samples = range(first_sample, max_num_samples*move_step+first_sample, move_step)
    plot_gamecube(average_over_games, error_over_games, samples)

def plot_gamecube(average_over_games, error_over_games, samples):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Get highest group bin count
    max_counts = max(np.ravel(average_over_games))
    # Get largest group size
    max_group_size = average_over_games.shape[1]
    # Sexy colors
    cmap = plt.get_cmap('jet')
    # Width of the bars
    num_samples = len(samples)
    width = 1.0 / (num_samples + 1.0)

    # Plot group size histogram
    for i in range(num_samples):
        counts = average_over_games[i, :]
        errors = error_over_games[i, :]
        # Can infer the correct bins by looking at the length of counts
        group_sizes = np.arange(1, len(counts) + 1) + width * i - 0.5 + width / 2

        ax.bar(group_sizes, counts, width, color = cmap(i / float(num_samples)), yerr = errors, \
                label = str(samples[i]) + ' moves')

    # Make the plot pretty
    ax.set_xlabel('Group sizes')
    ax.set_ylabel('Counts')
    ax.set_ylim(0.0, max_counts + 1)
    ax.set_xlim(0.5, max_group_size + 1)
    plt.legend(loc='upper right')

    # Set ticks to appear between bins and to label x positions of bins
    major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(major_locator)
    plt.tick_params(which='major', length = 0)
    minor_locator = FixedLocator(np.arange(0.5, max_group_size + 1.5, 1.0))
    ax.xaxis.set_minor_locator(minor_locator)

    # Draw the plot
    plt.show()

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


