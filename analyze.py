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
  return (position_black, position_white)

path = "badukmovies-pro-collection/1626/11/YasuiSantetsu-NakamuraDoseki3.sgf"
board, plays = load_game(path)
print get_positions(board, plays, [10])
