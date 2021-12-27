# ==============================================================================
"""PENTE : implementation of the "Penté" board game for two players"""
# ==============================================================================
__author__ = "Gwendal Prat and Clément Thion"
__version__ = "0.0"
__date__ = "2021-12-01"
# ==============================================================================
from ezTK import *
# ==============================================================================
class ConfigWin(Win):
  """configuration window for the "Penté" game"""
  def __init__(self, dim=8, score=5, nameA='Player A', nameB='Player B'):
    """create and show the configuration window"""
    font = 'Arial 20 bold'
    Win.__init__(self, title="ConfigWin", op=2, grow=True,bg='#98f4f3')  #config window
    # --------------------------------------------------------------------------
    Label(self,text='CONFIGURATION',width=23,bg='#1b32c5',fg='#819b93',font=font)
    # --------------------------------------------------------------------------
    frame = Frame(self, fold=2, flow='ES')
    #----
    Label(frame,text='Name of player A :',width=13,anchor='SW',grow=True,font='Arial 13 bold')
    self.p1 = Entry(frame)
    #----
    Label(frame,text='Name of player B :',width=13,anchor='SW',grow=True,font='Arial 13 bold')
    self.p2 = Entry(frame)
    #----
    Label(frame,text='Board Dimensions :',width=16,anchor='SW',grow=False,font='Arial 13 bold')
    self.dim = Scale(frame, scale=(dim, 16), flow='W', state=dim)
    #----
    Label(frame,text='Score for Victory :',width=16,anchor='SW',grow=False,font='Arial 13 bold')
    self.score = Scale(frame, scale=(score, 15), flow='W', state=score)
    # --------------------------------------------------------------------------
    self.gchrono = self.pchrono = self.voisinage = 1
    Button(frame,text='⚙',command=self.settings,bg='#1b32c5',fg='#819b93',
           font=font)
    Button(frame,text='?',command=self.rules,bg='#1b32c5',fg='#819b93',
           font=font)
    Button(frame,text='START',command=lambda: GameWin(self),bg='#1b32c5',
           fg='#819b93',font=font)
    # --------------------------------------------------------------------------
    self.loop()
  # ----------------------------------------------------------------------------
  def settings(self):
    """callback for the "POPUP" button"""

    self.gchrono = MessageDialog.askyesno('YES-NO', message='Add a global Chrono ?')
    
    self.pchrono = MessageDialog.askyesno('YES-NO', message='Add a player turn Chrono ?')
    
    self.voisinage = MessageDialog.askyesno('YES-NO', message='Set the switch rule ?')
    

  def rules(self):
    popup = Win(self, title='RULES', op=10,bg='#98f4f3')
    Label(popup, text= "This game is called Pente \n When one of the two players reaches the chosen victory score (set before the game starts), the game is over. \n To collect points, the players can either form a 5-tokens row or column, or set 2 tokens aside an opponent's token. \n Warning ! You cannot set a token on a cell if there's already a token, or if the cell is next to a token set the turn before.")
    Button(popup,text='UNDERSTOOD',command=popup.exit,fg='#819b93',bg='#1b32c5',
           font='Arial 20 bold')
    popup.wait()
#==============================================================================
class GameWin(Win):
  """game window for the "Penté" game"""
  def __init__(self, config):
    """create and show the game window, according to config parameters"""
    # ----GETTING SETTINGS------------------------------------------------------
    # ----Subsettings ----------------------------------------------------------
    self.gchrono = True  #Global chrono condition
    if config.gchrono == 0: self.gchrono = False
    self.pchrono = True  #Player chrono condition
    if config.pchrono == 0: self.pchrono = False
    self.voisinage = True  #True by default
    if config.voisinage == 0: self.voisinage = False
    # --------------------------------------------------------------------------
    self.dim = config.dim.state
    self.game = Game(self.dim)  # create kernel class and store it as attribute
    self.NameA = config.p1.state  #'NAME A'
    self.NameB = config.p2.state  #'NAME B'
    self.score = config.score.state
    # --------------------------------------------------------------------------
    config.exit()
    self.show()
  # ----------------------------------------------------------------------------
  def on_click(self, widget, code, mods):
    """callback function for all mouse click events"""
    #assert to click on the board and nowhere else
    if widget.master != self.frame or widget.index is None: return
    # ----------------------------------------------------------------------------
    if code != 'LMB': return
    else:  #when LeftMouseButton
      if widget.state != 0: return  #can only play on a black cell
      #--
      self.game.playerID=2-(1 + self.game.playerID) % 2#update player id in(1, 2)
      row, col = widget.index  #coordinates of clicked Label
      self.game.history.append((row, col))
      row0, col0 = self.game.history[-2]
      #---- rules applications : Game calls ==> updates of state matrice MStates
      self.game(row, col,self.game.playerID)  #update states matrice for player
      if self.voisinage: #if neighborhood rule is active in settings
          self.game.switch(row0, col0, True)  #erase last switch
          self.game.switch(row, col, False)  #new current switch
      self.game.align(row, col, self.game.playerID)
      self.game.capture(row, col, self.game.playerID)
      self.victory()
      #-- convert Game.L state into graphical animation
      self.tour.state = (self.tour.state + 1) % 2  #equivalent to do +=1
      for cell in self.game.Changes:  #update the grid
              self.frame[cell[0]][cell[1]].state = self.game(
                  cell[0], cell[1])
      #-- update score on display
      self.A['text'] = f'{self.NameA} \n {self.game.score[0]}'
      self.B['text'] = f'{self.NameB} \n {self.game.score[1]}'
      self.game.Changes = []
  # ----------------------------------------------------------------------------
  def show(self):
    """show current game board by setting state defined for each grid cell"""
    # --------------------------------------------------------------------------
    Win.__init__(self,title="Pente",op=2,fold=1,flow='ES',click=self.on_click,bg='#98f4f3',
                 grow=False)  #creates window
    font2 = 'Arial 20 bold'
    images = tuple(Image(file=f"{id}.gif")for id in range(4))  #import image
    # --------------------------------------------------------------------------
    if self.gchrono == True:
      Label(self,text = 'Global Time :', font="Arial 16 bold underline")
      self.globalchrono = Label(self, text=0, font="Arial 16 bold")

    time = Frame(self,fold=2,flow='ES')
    if self.pchrono == True :
      Label(time,text = f"{self.NameA}'s time left", font="Arial 16 bold")
      Label(time,text = f"{self.NameB}'s time left", font="Arial 16 bold")
      self.chrono1 = Label(time, text=120, font='Arial 16 bold',width=3)
      self.chrono2 = Label(time, text=120, font='Arial 16 bold',width=3)
      
    frameStat = Frame(self, flow='ES')
    self.A = Label(frameStat,font=font2,fg='blue',border=2,width=10,
          text=(f'{self.NameA}\n{self.game.score[0]}'))#Player A informations
    self.tour = Label(frameStat,font='Arial 35 bold',width=2,
          text=('A', 'B'), bg='Black',fg=('#6069f5', '#50db20'))  #Current player turn
    self.B = Label(frameStat, font=font2,fg='green',border=2,width=10,
          text=(f'{self.NameB}\n{self.game.score[1]}'))#Player B informations
    # --------------------------------------------------------------------------
    self.frame = Frame(self, fold=self.dim, flow='ES')  #grid container
    for n in range(self.dim * self.dim):  #Creates the grid
      grid = Label(self.frame, image=images)
    # --------------------------------------------------------------------------
    self.after(2000,self.tick);self.loop()
  # ----------------------------------------------------------------------------
  def victory(self):
    """play victory animation"""
    if self.game.score[0] >= self.score :
      self.winner = self.NameA
      self.game.over=True
    elif self.game.score[1] >= self.score:
      self.winner = self.NameB
      self.game.over=True
      
    if self.game.over:
      for r in range(self.dim):
        for c in range(self.dim):
          self.frame[r][c].state = 3
      # --Win-- 
      popup = Win(self, title='VICTORY', op=10,bg='#98f4f3')
      Label(popup, text="Game Over",font = 'Arial 30 bold underline')
      if self.gchrono == True : 
        Label(popup, text= f"The winner is {self.winner}. This game lasted {self.globalchrono['text']} seconds.")
      else:
        Label(popup, text= f"The winner is {self.winner}.")
      # --Frame--
      frame = Frame(popup, fold=2)
      Label(frame, text = f"{self.NameA}'s results :",font = 'Arial 15 underline')
      Label(frame, text = f"{self.NameB}'s results :",font = 'Arial 15 underline')
      Label(frame, text = f"{self.game.score[0]} points")
      Label(frame, text = f"{self.game.score[1]} points")
      if self.pchrono == True :
        Label(frame, text = f"{self.chrono1['text']} second(s) remaining")
        Label(frame, text = f"{self.chrono2['text']} second(s) remaining")
      # --//--
      Button(popup,text='NEW GAME',command=self.new_game,bg='#1b32c5', fg='#819b93',
             font='Arial 20 bold')
      popup.wait()
  # ----------------------------------------------------------------------------
  def new_game(self):
    """New game launcher"""
    self.exit()
    ConfigWin()
  # ----------------------------------------------------------------------------
  def tick(self):
    """Manage chrono"""
    self.victory()  #stop the chrono if there's a winner

    if self.pchrono==True :
      if self.chrono1['text']==0 :
        self.game.over=True
        self.winner = self.NameB
        self.victory()
        return
      if self.chrono2['text']==0:
        self.game.over=True
        self.winner=self.NameA
        self.victory()
        return

    if self.gchrono == True and self.pchrono == False:
      self.globalchrono['text']+=1
      self.after(1000,self.tick)

    elif self.gchrono == False and self.pchrono == True:
      if self.tour.state == 0:
        self.chrono1['text'] = self.chrono1['text'] -1
        if self.chrono1['text'] == 20:self.chrono1['fg'] = 'red'
        self.after(1000, self.tick)
      else:
        self.chrono2['text'] = self.chrono2['text'] -1 
        if self.chrono2['text'] == 20: self.chrono2['fg'] = 'red'
        self.after(1000, self.tick)

    elif self.gchrono==True and self.pchrono==True:
      self.globalchrono['text']+=1
      if self.tour.state == 0:
        self.chrono1['text'] = self.chrono1['text'] -1
        if self.chrono1['text'] == 20:self.chrono1['fg'] = 'red'
        self.after(1000, self.tick)
      else:
        self.chrono2['text'] = self.chrono2['text'] -1 
        if self.chrono2['text'] == 20: self.chrono2['fg'] = 'red'
        self.after(1000, self.tick)
# ==============================================================================
class Game(object):
  """kernel class for the "Penté" game"""
  def __init__(self, dim=8):
    """create and initialize the grid data structure"""
    self.over = False  #game over indicator
    self.dim = dim
    self.history = [(0, 0)]#storages every players moves from start to game over
    self.MState = [dim * [0].copy()for _ in range(dim)]#bijection with grid states
    self.Changes = []  #list of points modified by current move
    self.score = [0, 0]  #storage of players score
    self.playerID = 2  #last player who played, 2 by default for the first move

  # ----------------------------------------------------------------------------
  def __call__(self, row, col, state=None):
    """get or set state for provided grid cell"""
    if state == None: return self.MState[row][col]  #return cell state
    else:  #change cell state
      assert isinstance(state, int), "state must be an integer"
      self.MState[row][col] = state % 4
      self.Changes.append((row, col))

  # ----------------------------------------------------------------------------
  def switch(self, row, col, valid=True):
    """switch valid/invalid state for neighborhood of provided grid cell"""
    
    #----Neighborhood
    neighborhood = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1),
                    (-1, 0), (-1, -1)]
    for x in neighborhood:
      xrow, xcol = row + x[0], col + x[1]  # x,y neighbor coordinates
      if not 0 <= xrow < self.dim or not 0 <= xcol < self.dim:
        continue  #if out of grid
      elif not valid and self.MState[xrow][xcol] == 0:  #if black cell
        self(xrow, xcol, 3)  #--> grey
      elif valid and self.MState[xrow][xcol] == 3:  #if grey cell
        self(xrow, xcol, 0)  #--> black

  # ----------------------------------------------------------------------------
  def align(self, row, col, playerID):
    """check if provided move creates align config and return score update"""
    gain = 0
    # return 5 points for each detected align pattern
    hori = ''.join([str(token) for token in self.MState[row]])
    verti = ''.join([str(rowlist[col]) for rowlist in self.MState])
    diagup = ''
    diagdown = ''
    #----DIAGUP
    #----OPTIMISATION A FAIRE AVEC DU MIN ET DU MAX POUR FACTORISER LES DEUX CAS
    if row+col<=self.dim-1:
        for irow in range(0, col+row+1):
            jcol=col+row-irow
            diagup += str(self(irow, jcol))
    else:
        for irow in range(row+col-self.dim+1, self.dim):
            jcol=row+col-irow
            diagup += str(self(irow, jcol))        
    #----DIADOWN
    shift = row - col
    if shift < 0:
      rowshift = 0
      colshift = abs(shift)  #below diagdown
    else:
      rowshift = shift
      colshift = 0  #under diagdown
    coldiag = colshift
    for rowdiag in self.MState[0 + rowshift:self.dim - colshift]:
      diagdown += str(rowdiag[coldiag])
      coldiag += 1
    #---- detecting alignment 
    for vect in (hori, verti, diagup, diagdown):
      if 5 * str(playerID) in vect: gain += 5
    self.score[playerID - 1] += gain  #update score

  # ----------------------------------------------------------------------------
  def capture(self, row, col, playerID):
    """check if provided move creates capture config and return score update"""
    # return 1 point for each detected capture pattern
    print('CAPTURE!')
    gain=0 #initial gain
    hori = ''.join([str(token) for token in self.MState[row]
                    #[col-max(0, col-3) : col+min(self.dim, col+3)] #take 5-longue intervalle around col
                    ]) #ensure intervalle valid
    print('hori', hori)
    verti = ''.join([str(rowlist[col]) for rowlist in self.MState])
    adversaryID = 2-(1+playerID)%2
    patern = str(playerID)+2*str(adversaryID)+str(playerID) #2112 or 1221
    #--get every patern index in a list
    patern_indexs=[]
    for direction in (hori, verti): #check every directions
        tampon= [index for index in range(len(direction))
                           if direction.startswith(patern, index)] #True if a.index(patern)==index
        if len(tampon)!=0: 
            for item in tampon: patern_indexs.append(item)
    print('patern_indexs', patern_indexs)
    #----update score 
    gain += len(patern_indexs) #one point for each patern
    self.score[playerID - 1] += gain  
# ==============================================================================
if __name__ == "__main__":
  ConfigWin()
# ==============================================================================
