# ==============================================================================
"""PENTE : implementation of the "Penté" board game for two players"""
# ==============================================================================
__author__  = "Gwendal Prat and Clément Thion"
__version__ = "0.0"
__date__    = "2021-12-01"
# ==============================================================================
from ezTK import *
# ==============================================================================
class ConfigWin(Win):
  """configuration window for the "Penté" game"""
  def __init__(self, dim=8, score=5, nameA='Player A', nameB='Player B'):
    """create and show the configuration window"""
    font='Arial 20 bold'
    Win.__init__(self,title="ConfigWin", op=2,grow=True) #config window
    # --------------------------------------------------------------------------
    Label(self,text='CONFIGURATION',width=23,bg='Black',fg='White',font=font)
    # --------------------------------------------------------------------------
    self.frame = Frame(self, fold = 2, flow='ES')

    Label(self.frame, text='Name of player A :', width=13, anchor='SW',grow=True) 
    self.p1 = Entry(self.frame)

    Label(self.frame, text='Name of player B :', width=13, anchor='SW',grow=True)
    self.p2 = Entry(self.frame)

    Label(self.frame,text='Board Dimensions :',width=16,anchor='SW',grow=False)
    self.dim = Scale(self.frame, scale=(dim,16), flow='W',state=dim)
  
    Label(self.frame,text='Score for Victory :',width=16,anchor='SW',grow=False)
    self.score = Scale(self.frame, scale=(score,15), flow='W', state=score)
    # --------------------------------------------------------------------------
    Button(self.frame,text='START', command = lambda : GameWin(self),bg='Black',
    fg='White',font=font)
    # --------------------------------------------------------------------------
    self.loop()
# ==============================================================================
class GameWin(Win):
  """game window for the "Penté" game"""
  def __init__(self, config):
    """create and show the game window, according to config parameters"""
    # ----GETTING SETTINGS------------------------------------------------------
    self.NameA = config.p1.state #'NAME A'#cwin.p1.state
    self.A_Counter=0  #Player A points counter ----- Not changeable for now
    self.NameB= config.p2.state#'NAME B' #cwin.p2.state
    self.B_Counter=0  #Player B points counter ----- Not changeable for now
    self.dim = config.dim.state #cwin.dim.state
    self.score = config.score.state #cwin.score.state
    config.exit()
    self.over = False #game over indicator
    # --------------------------------------------------------------------------
    self.game = Game(self.dim) # create kernel class and store it as attribute
    self.show()
  # ----------------------------------------------------------------------------
  def on_click(self, widget, code, mods):
    """callback function for all mouse click events"""
    #assert to click on the board and nowhere else
    if widget.master != self.frame or widget.index is None:return
  # ----------------------------------------------------------------------------
    if code =='LMB': #when left mouse button
      if widget.state != 0 :return  #can only play on a black cell
      if self.tour['text'] =='A': widget.state = 1
      if self.tour['text'] =='B': widget.state = 2
      self.tour.state +=1
      print('je clique osti de calisse de tabarnak')
      self.victory()
  # ----------------------------------------------------------------------------
  def show(self):
    """show current game board by setting state defined for each grid cell"""
    # --------------------------------------------------------------------------
    Win.__init__(self,title="Pente", op=2, fold=3, click=self.on_click) #creates window
    font2='Arial 20 bold'
    # --------------------------------------------------------------------------
    self.A = Label(self, font=font2, height=1, border=2,
        text = (f'{self.NameA} \n {self.A_Counter}'))#Player A informations

    self.tour = Label(self,font='Arial 35 bold' , height=1,width=1,
        text = ('A','B'),bg ='Black' , fg = 'White')#Current player turn

    self.B = Label(self, font=font2, height=1, border=2,
        text = (f'{self.NameB} \n {self.A_Counter}'))#Player B informations
    # --------------------------------------------------------------------------
    self.frame = Frame(self, fold = self.dim, flow='ES')#grid container
    images = tuple(Image(file=f"{id}.gif") for id in range(4))#import images
    for n in range(self.dim * self.dim):  #Creates the grid
      grid = Label(self.frame, image=images)
    # --------------------------------------------------------------------------
    self.loop()
  # ----------------------------------------------------------------------------
  def victory(self):
    """play victory animation"""
    if self.over:
      for r in range(self.dim):
        for c in range(self.dim):
          self.frame[r][c].state =3
# ==============================================================================
class Game(object):
  """kernel class for the "Penté" game"""
  def __init__(self, dim=8):
    """create and initialize the grid data structure"""
    L = dim*[dim*[0]]
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
  #ConfigWin()
  Game()
# ==============================================================================
