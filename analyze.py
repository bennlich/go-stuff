#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
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
  '''
  # aggregate board positions in here
  positions = []
  # only iterate through plays up to
  # the latest move we're interested in
  last_move = np.amax(move_numbers)
  relevant_plays = plays[:last_move+1]
  for move_number, play in enumerate(relevant_plays):
    colour, move = play
    if move is None:
      continue
    row, col = move

    try:
      board.play(row, col, colour)
    except ValueError:
      raise StandardError("illegal move in sgf file")

    if move_number in move_numbers:
      positions.append(board_to_numpy_arrays(board))

  return positions

def board_to_numpy_arrays(board):
  '''
  '''
  points = board.list_occupied_points()
  plays_white = [ point[1] for point in points if point[0] is 'w' ]
  plays_black = [ point[1] for point in points if point[0] is 'b' ]
  coords_white = zip(*plays_white)
  coords_black = zip(*plays_black)
  position_white = np.zeros([19, 19])
  position_black = np.zeros([19, 19])
  position_white[coords_white] = 1
  position_black[coords_black] = 1
  return position_black, position_white

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

##################################################

if __name__ == '__main__':

    print directory_map("badukmovies-pro-collection", lambda x: x)

    # # Load boards at specified move
    # path = "badukmovies-pro-collection/1626/11/YasuiSantetsu-NakamuraDoseki3.sgf"
    # board, plays = load_game(path)
    # b_board, w_board = get_positions(board, plays, [100])[0]

    # # Check group sizes
    # b_bins, b_counts = group_finder.get_group_hists(b_board)
    # w_bins, w_counts = group_finder.get_group_hists(w_board)
    # combined_bins, combined_counts = group_finder.combine_hists(b_bins, b_counts, w_bins, w_counts)

    # # Plot group size histogram
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)

    # ax.scatter(b_bins, b_counts, color = 'black', label = 'Black')
    # ax.scatter(w_bins, w_counts, facecolors = 'none', label = 'White')
    # ax.scatter(combined_bins, combined_counts, color = 'gray', label = 'Combined')

    # ax.set_xlabel('Group sizes')
    # ax.set_ylabel('Counts')
    # ax.set_ylim(-0.5, max(combined_counts) + 1)
    # plt.legend(loc='upper right')

    # plt.show()

