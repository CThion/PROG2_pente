# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 17:20:35 2022

@author: geeka
"""

# ==============================================================================
"""GamePeg : kernel class for the solitaire peg game"""
# ==============================================================================
__author__  = "Christophe Schlick"
__version__ = "1.0"
__date__    = "2021-10-15"
__usage__   = ""
# ------------------------------------------------------------------------------
from ezCLI import testcode
# ------------------------------------------------------------------------------
# define name and inital peg positions for all game configurations
# each configuration is encoded as a string composed of four different chars :
# ':' = new line, ' ' = invalid cell, 'O' = hole, 'X' = peg
configs = dict(
 cross1  ='         :    O    :    X    :    X    : OXXXXXO :    X    :    X    :    O    :         ',
 cross2  ='         :   XXX   :   XXX   : XXXXXXX : XXXOXXX : XXXXXXX :   XXX   :   XXX   :         ',
 cross3  ='   XXX   :   XXX   :   XXX   :XXXXXXXXX:XXXXOXXXX:XXXXXXXXX:   XXX   :   XXX   :   XXX   ',
 cross4  ='  XXXXX  :  XXXXX  :XXXXXXXXX:XXXXXXXXX:XXXXOXXXX:XXXXXXXXX:XXXXXXXXX:  XXXXX  :  XXXXX  ',
 square1 ='         :         :  XXXXX  :  XXXXX  :  XXOXX  :  XXXXX  :  XXXXX  :         :         ',
 square2 ='         : XXXXXXX : XXXXXXX : XXXXXXX : XXXOXXX : XXXXXXX : XXXXXXX : XXXXXXX :         ',
 square3 ='XXXXXXXXX:XXXXXXXXX:XXXXXXXXX:XXXXXXXXX:XXXXOXXXX:XXXXXXXXX:XXXXXXXXX:XXXXXXXXX:XXXXXXXXX',
 diamond1='         :    O    :   OXO   :  OXXXO  : OXXOXXO :  OXXXO  :   OXO   :    O    :         ',
 diamond2='    O    :   OXO   :  OXXXO  : OXXXXXO :OXXXOXXXO: OXXXXXO :  OXXXO  :   OXO   :    O    ',
 diamond3='         :   XXX   :  XXXXX  : XXXXXXX : XXXOXXX : XXXXXXX :  XXXXX  :   XXX   :         ')
# ------------------------------------------------------------------------------
class GamePeg(object):
  """kernel class for the solitaire peg game"""
  # ----------------------------------------------------------------------------
  def __init__(self, config='cross1'):
    """initialize 'self' by creating the board with chosen game configuration"""
    self.configs = configs; self.reset(config)
  # ----------------------------------------------------------------------------
  def __repr__(self):
    """return object representation for 'self'"""
    return f"{type(self).__name__}(config='{self.config}')"
  # ----------------------------------------------------------------------------
  def __str__(self):
    """return string representation for 'self'"""
    board = [[' ' for col in range(self.size)] for row in range(self.size)]
    for row,col in self.board: board[row][col] = self.board[row,col]
    return '\n'.join(' '.join(line) for line in board)
  # ----------------------------------------------------------------------------
  def __eq__(self, peer):
    """test equality between 'self' and 'peer'"""
    return repr(self) == repr(peer)
  # ----------------------------------------------------------------------------
  def __call__(self, row, col, value=None):
    """set or get the board cell at coordinates (col,row)"""
    if (row, col) not in self.board: return ' ' # invalid cell
    if value is None: return self.board[row,col] # get current value for cell
    else: self.board[row,col] = value # set new value for cell
  # ----------------------------------------------------------------------------
  def reset(self, config=''):
    """reset the board and set game configuration according to 'config'"""
    if not config: config = self.config # reset with previous configuration
    assert config in configs, f"{config} = invalid game configuration"
    board = self.configs[config] # get board string from selected configuration
    self.config, self.size = config, board.index(':') # store board parameters
    self.pegs = board.count('X') # count initial number of pegs on board
    # get coords and values for all valid board cells and store them as a dict
    self.board = dict(((r,c),v) for r,line in enumerate(board.split(':'))
      for c,v in enumerate(line) if v != ' ')
  # ----------------------------------------------------------------------------
  def move(self, row, col): 
    """apply move to peg located at (col,row)"""
    if self(row,col) != 'X': return False # no peg in current cell
    # order of priority for move directions : left, right, up, down
    if   self(row,col-1) == 'X' and self(row,col-2) == 'O': dr, dc =  0,-1
    elif self(row,col+1) == 'X' and self(row,col+2) == 'O': dr, dc =  0, 1   
    elif self(row-1,col) == 'X' and self(row-2,col) == 'O': dr, dc = -1, 0
    elif self(row+1,col) == 'X' and self(row+2,col) == 'O': dr, dc =  1, 0
    else: return False # no valid move for selected peg
    # change the state for the three cells involved in the selected move
    self(row,col, 'O'); self(row+dr,col+dc, 'O'); self(row+2*dr,col+2*dc, 'X')
    self.pegs -= 1; return True # update number of remaining pegs
# ==============================================================================
if __name__ == "__main__": # testcode for class 'GamePeg'
  code = r'''
a = GamePeg()
a
a.pegs, a.size, a.board
str(a)

a(4,5), a(4,6), a(4,7), a(0,0), a(0,9), a.pegs
a.move(4,5), a.move(4,6), a.move(4,7)
a(4,5), a(4,6), a(4,7), a(0,0), a(0,9), a.pegs
str(a)

a.reset()
str(a)

a.reset('cross2')
str(a)

a.reset('cross3')
str(a)

a.reset('cross4')
str(a)

a.reset('square1')
str(a)

a.reset('square2')
str(a)

a.reset('square3')
str(a)

a.reset('diamond1')
str(a)

a.reset('diamond2')
str(a)

a.reset('diamond3')
str(a)

a.reset('zzz')
'''; testcode(code)
# ==============================================================================