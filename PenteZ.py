# ==============================================================================
"""PENTE : implementation of the "Penté" board game for two players"""
# ==============================================================================
__author__  = "Christophe Schlick"
__version__ = "0.0" # skeleton version
__date__    = "2021-10-15"
# ==============================================================================
from ezTK import *
# ==============================================================================
class ConfigWin(Win):
  """configuration window for the "Penté" game"""
  def __init__(self, dim=8, score=5, nameA='Player A', nameB='Player B'):
    """create and show the configuration window"""
    self.win = Win(title="ConfigWin", op=2,grow=True) #config window
    # --------------------------------------------------------------------------
    font2='Arial 20 bold'
    Label(self.win,text='CONFIGURATION',width=23,bg='Black',fg='White',
          font=font2)
    # --------------------------------------------------------------------------
    self.frame = Frame(self.win, fold = 2, flow='ES')

    Label(self.frame, text='Name of player A :',width=13, anchor='SW',
          grow=True)
    self.win.p1 = Entry(self.frame)

    Label(self.frame, text='Name of player B :', width=13, anchor='SW',
          grow=True)
    self.win.p2 = Entry(self.frame)

    Label(self.frame, text='Board Dimensions :', width=16, anchor='SW',
          grow=False)
    self.win.dim = Scale(self.frame, scale=(dim,16), flow='W',state=dim)
  
    Label(self.frame, text='Score for Victory :', width=16, anchor='SW',
          grow=False)
    self.win.score = Scale(self.frame, scale=(score,15), flow='W', state=score)
    # --------------------------------------------------------------------------
    board = GameWin(self)
    Button(self.frame,text='START',command= board.show(), bg='Black',fg='White',
           font=font2)
    # --------------------------------------------------------------------------
    self.win.loop()
# ==============================================================================
class GameWin(Win):
  """game window for the "Penté" game"""
  def __init__(self, config):
    """create and show the game window, according to config parameters"""
    # self.game = Game(dim) # create kernel class and store it as attribute
  # ----------------------------------------------------------------------------
  def on_click(self, widget, code, mods):
    """callback function for all mouse click events"""
  # ----------------------------------------------------------------------------
  def show(self):
    """show current game board by setting state defined for each grid cell"""
  # ----------------------------------------------------------------------------
  def victory(self):
    """play victory animation"""
# ==============================================================================
class Game(object):
  """kernel class for the "Penté" game"""
  def __init__(self, dim=8):
    """create and initialize the grid data structure"""
  # ----------------------------------------------------------------------------
  def __call__(self, row, col, state=None):
    """get or set state for provided grid cell"""
  # ----------------------------------------------------------------------------
  def switch(self, row, col, valid=True):
    """switch valid/invalid state for neighborhood of provided grid cell"""
  # ----------------------------------------------------------------------------
  def align(self, row, col, player):
    """check if provided move creates align config and return score update"""
    # return 5 points for each detected align pattern
  # ----------------------------------------------------------------------------
  def capture(self, row, col, player):
    """check if provided move creates capture config and return score update"""
    # return 1 point for each detected capture pattern
# ==============================================================================
if __name__ == "__main__":
  ConfigWin()
# ==============================================================================
