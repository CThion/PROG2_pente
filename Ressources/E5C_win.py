# ==============================================================================
"""WIN : demo program for window manipulations"""
# ==============================================================================
__author__  = "Christophe Schlick"
__version__ = "3.0" # toggle between two different master windows
__date__    = "2021-09-15"
# ==============================================================================
from ezTK import *
# ------------------------------------------------------------------------------
class ConfigWin(Win):
  """configuration window"""
  # ----------------------------------------------------------------------------
  def __init__(self):
    """create the config window and pack the widgets"""
    Win.__init__(self, title='CONFIG', grow=False, fold=2, op=2) # config window
    # --------------------------------------------------------------------------
    Label(self, text='Number of rows :', grow=False, width=13, anchor='SW')
    Scale(self, scale=(1,8), flow='W')
    Label(self, text='Number of cols :', grow=False, width=13, anchor='SW')
    Scale(self, scale=(1,8), flow='W')
    Button(self, text='NEW GRID', command=lambda: GridWin(self))
    # --------------------------------------------------------------------------
    self.rowscale, self.colscale = self[0][1], self[1][1]; self.loop()
# ------------------------------------------------------------------------------
class GridWin(Win):
  """grid window"""
  # ----------------------------------------------------------------------------
  def __init__(self, win):
    """create the grid window and pack the widgets"""
    rows, cols = win.rowscale.state, win.colscale.state # get grid size
    win.exit() # exit config window (only after having read state of scales)
    Win.__init__(self, title='GRID', fold=cols, bg='#000', op=2) # grid window
    # --------------------------------------------------------------------------
    images = tuple(Image(file=f"Z{color}.gif") for color in 'RGBCMY')
    for loop in range(rows*cols): Label(self, image=images, state=loop)
    # --------------------------------------------------------------------------
    self.loop(); ConfigWin() # relaunch ConfigWin when GridWin is closed
# ==============================================================================
if __name__ == "__main__": # testcode for class 'DemoWin'
  ConfigWin()
# ==============================================================================
