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

    # Count the frequency of each group size
    size_counts, size_bins = np.histogram(group_sizes, np.arange(1, max(group_sizes) + 2))
    size_bins = size_bins[0:-1]

    return size_bins, size_counts

b_board1 = np.array([[1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 0, 1, 1]])

print(get_group_hists_helper(b_board1))


