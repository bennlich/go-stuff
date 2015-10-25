#!/usr/bin/env python

import numpy as np
from scipy.ndimage.measurements import label

bBoard1 = np.array([[1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 0, 1, 1]])
#wBoard1 = np.zeros(19, 19)

#def getGroupHists(bBoard, wBoard):
#    """
#    Gets number of groups for black and white players.
#    """

def getGroupHistsHelper(board):
    """
    Gets number of groups in a board.
    """
    # Label and get number of connected components in board
    groups, numGroups = label(board)
    # Store size of each group
    groupSizes = []

    # Loop over groups' number labels
    for gNum in range(1, numGroups + 1):
        # Count number of pieces in group gNum
        groupSizes.append(len([1 for row in groups for piece in row if piece == gNum]))

    # Count the frequency of each group size
    sizeCounts, sizeBins = np.histogram(groupSizes, np.arange(1, max(groupSizes) + 2))
    sizeBins = sizeBins[0:-1]

    return sizeBins, sizeCounts

print(getGroupHistsHelper(bBoard1))


