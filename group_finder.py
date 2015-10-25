#!/usr/bin/env python

import numpy as np
from scipy.ndimage.measurements import label

#def getGroupHists(bBoard, wBoard):
#    """
#    Gets number of groups for black and white players.
#    """

def get_group_hists(board):
    """
    Gets number of groups in a board.
    """
    # Label and get number of connected components in board
    groups, num_groups = label(board)
    # Store size of each group
    group_sizes = []

    # Loop over groups' number labels
    for g_num in range(1, num_groups + 1):
        # Count number of pieces in group gNum
        group_sizes.append(len([1 for row in groups for piece in row if piece == g_num]))

    # Count the frequency of each group size.  Could be more efficient.
    size_counts, size_bins = np.histogram(group_sizes, np.arange(1, max(group_sizes) + 2))
    size_bins = size_bins[0:-1]

    return size_bins, size_counts

def combine_hists(bins1, counts1, bins2, counts2):
    max_length = np.amax([counts1.size, counts2.size])
    new_hist_1 = np.zeros(max_length)
    new_hist_2 = np.zeros(max_length)
    new_hist_1[:counts1.size] = counts1
    new_hist_2[:counts2.size] = counts2
    combined_hist = new_hist_1 + new_hist_2
    combined_bins = bins1 if bins1.size > bins2.size else bins2

    return combined_bins, combined_hist

##################################################

if __name__ == '__main__':
    b_board1 = np.array([[1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 1]])

    print(get_group_hists(b_board1))


