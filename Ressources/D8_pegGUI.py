# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 17:21:27 2022

@author: geeka
"""

# ==============================================================================
"""GUIPeg : GUI (= graphical user interface) class for the solitaire peg game"""
# ==============================================================================
__author__  = "Christophe Schlick"
__version__ = "1.0"
__date__    = "2021-10-15"
# ==============================================================================
from ezTK import *
from D8_peg import GamePeg
from random import choice
# ------------------------------------------------------------------------------
class GUIPeg(Win):
  """GUI class for the solitaire peg game"""
  # ----------------------------------------------------------------------------
  def __init__(self):
    """create the main window and pack the widgets"""
    Win.__init__(self, title='PEG GAME', op=5, click=self.on_click, grow=False)
    self.game = GamePeg() # create instance of the kernel class
    configs = tuple(self.game.configs) # get all config names from kernel class
    # --------------------------------------------------------------------------
    frame = Frame(self, font='Arial 14')
    Label(frame, text='Current config :')
    Spinbox(frame, values=configs, width=8, justify='center')
    Button(frame, text='RESET', command=self.reset)
    Label(frame, width=12, border=2)
    # --------------------------------------------------------------------------
    size, colors = self.game.size, ('#CCC','#FFF','#08F') # cell colors
    board = Frame(self, bg=colors[0], fold=size, border=2)
    for loop in range(size*size): Brick(board, width=64, height=64, bg=colors)
    # --------------------------------------------------------------------------
    self.board, self.config, self.message = board, frame[1], frame[3]
    self.reset(); self.loop()
  # ----------------------------------------------------------------------------
  def on_click(self, widget, code, mods):
    """callback function for all 'mouse click' events"""
    if widget.master != self.board or widget.index is None:
      return # nothing to do if the selected widget is not a board cell
    if self.game.move(*widget.index): self.show() # apply valid move
    else: self.message['text'] = "Invalid move" # show error message
    self.victory() # check if victory and play victory animation when done
  # ----------------------------------------------------------------------------
  def reset(self):
    """callback function for the RESET button"""
    for line in self.board: # loop over board and clear all cells
      for cell in line: cell.state = 0; cell['relief'] = 'flat'
    self.game.reset(self.config.state); self.show() # reset game configuration
  # ----------------------------------------------------------------------------
  def show(self):
    """show new game board by updating states of all cells"""
    board, states = self.game.board, {' ':0, 'O':1, 'X':2}
    for row, col in board: # loop over coords of valid cells
      self.board[row][col].state = states[board[row,col]] # update cell state
      self.board[row][col]['relief'] = 'solid' # update cell relief
    self.message['text'] = f"Pegs = {self.game.pegs}" # update message
  # ----------------------------------------------------------------------------
  def victory(self):
    """show victory animation"""
    if self.game.pegs != 1: return # no victory yet
    row, col = choice(tuple(self.game.board)) # select random cell on board
    self.board[row][col].state = 3-self.board[row][col].state # reverse state
    self.after(10, self.victory) # launch 'victory' to get next animation step
# ==============================================================================
if __name__ == "__main__": # testcode for class 'GUIPeg'
  GUIPeg()
# ==============================================================================