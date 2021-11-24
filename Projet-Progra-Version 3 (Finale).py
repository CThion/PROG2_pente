# ==============================================================================
"""Python project : Treasure Hunter"""
# ==============================================================================
__author__  = "Gwendal et Elouan"
__version__ = "3.0" # Makes the game playable, with point counters
                    # and a results window with new game launcher
__date__    = "2020-05-30"
# ==============================================================================
from ezTK import *
from random import randrange
# ==============================================================================
def effet_config():
  """Creates the grid and starts the game, using the previous settings"""
  global win2
  win2 = Win(title='Treasure Hunter', op=2, click = on_click,fold=3)

  font2,font3= 'Arial 20 bold','Arial 35 bold'
  # ----------------------------------------------------------------------------
  global goal   #Saves the number of treasures
  goal = win.goalscale.state
  global col    #Saves the number of columns
  col = win.colscale.state
  global row    #Saves the number of rows
  row = win.rowscale.state

  win2.Aname=win.p1.state
  win2.Bname=win.p2.state
  win2.Acounter = 0
  win2.Bcounter = 0
  
  win2.A = Label(win2, font=font2, height=1, border=2,
        text = ('%s \n %s' % (win2.Aname,win2.Acounter)))

  win2.tour = Label(win2,font=font3 , height=1,width=1,
        text = ('A','B','B','A'),bg ='Black' , fg = 'White')

  win2.B = Label(win2, font=font2, height=1, border=2,
        text = ('%s \n %s' % (win2.Bname,win2.Bcounter)))
  # ----------------------------------------------------------------------------
  win2.frame = Frame(win2, fold=col,flow='ES')
  
  for n in range((row)*(col)):  #Creates the grid
    grid = Label(win2.frame, text='', bg='White',border=2, width=2, height=1)
  # ----------------------------------------------------------------------------
  index = win2.index
  randtreasure()
  # ----------------------------------------------------------------------------
  win.exit()
  win3.exit()
# ==============================================================================
def randtreasure ():
  """Sets the treasures and saves their location"""
  global coordx
  global coordy
  coordx = []
  coordy = []
  
  for n in range (goal):

    xa = randrange(row)
    for i in range(n):
      while coordx[i]==xa:
        xa=randrange(row) #Make sure 2 treasures are not on the same spot
    coordx.append(xa)

    ya = randrange(col)                     
    coordy.append(ya)
# ==============================================================================
def coordcases (index):
  """Index function for any widget"""
  global xb,yb
  xb,yb = index
# ==============================================================================
def distance():
  """Gives the distance between the nearest treasure and the widget clicked"""
  listedist=[]
  for i in range(goal):
    listedist.append(abs(xb - coordx[i]) + abs(yb - coordy[i]))
  return min(listedist)
# ==============================================================================
def on_click(widget,code,mods):
  """Callback function for all mouse click events"""
  if widget.master != win2.frame or widget.index is None:
    return
  
  coordcases (widget.index) #Gives the widget coords with a click
  # ----------------------------------------------------------------------------  
  points=0
                        #Gives each widget a value and a color when clicked
  if code == 'LMB':
      
      widget['text']=distance()
      if distance() == 0 :
          widget['bg']='Black'
          points=36
      elif distance()<3:
          widget['bg']='Red'
          points=25
      elif distance()<6:
          widget['bg']='Yellow'
          points=16
      elif distance()<10:
          widget['bg']='Lime'
          points=9
      elif distance()<15:
          widget['bg']='Cyan'
          points=4
      elif distance()>14:
          widget['bg']='Grey'
          points=1

  if win2.tour['text']=='A':win2.tour.state+=1; win2.Acounter+=points
  elif win2.tour['text']=='B':win2.tour.state+=1; win2.Bcounter+=points
  win2.A['text'] = ('%s \n %s' % (win2.Aname,win2.Acounter))
  win2.B['text'] = ('%s \n %s' % (win2.Bname,win2.Bcounter))
  # ----------------------------------------------------------------------------
  i=0
  if code == 'LMB':
    for r in range(row):
      for c in range(col):
        if win2.frame[r][c]['bg']=='Black':i+=1
                                     #Reveals the grid when the game is over
  if i == goal :
    a = win2.Acounter
    b = win2.Bcounter
    for r in range(row):
      for c in range(col):
        if win2.frame[r][c]['bg']=='White':
          on_click(win2.frame[r][c], code, mods)
    win2.Acounter = a
    win2.Bcounter = b
    win2.A['text'] = ('%s \n %s' % (win2.Aname,win2.Acounter))
    win2.B['text'] = ('%s \n %s' % (win2.Bname,win2.Bcounter))

    win2.after(5000,game_over)  #Opens the results window after 5 seconds
# ==============================================================================
def game_over():
  """Results window and new game launcher"""
  win2.exit()
  global win3
  win3=Win(title='Treasure Hunter',grow=True, op=4)    
  # ---------------------------------------------------------------------------- 
  Label(win3, text='GAME OVER',bg='Black', fg='White', font = 'Arial 20 bold')
  
  results = Frame(win3,fold=2)
  Label(results,text=('%s \n %s' % (win2.Aname, win2.Acounter)),border=2,
        width=4, font = 'Arial 20 bold')
  Label(results,text=('%s \n %s' % (win2.Bname, win2.Bcounter)),border=2,
        width=4, font = 'Arial 20 bold')

  Label(win3, text='Do you want to start a new game ?', font = 'Arial 20 bold')
  
  choice = Frame(win3,fold=2)
  Button(choice, text='YES',command=config, font = 'Arial 20 bold', bg= 'Lime',
         fg = 'White')
  Button(choice, text='NO',command=win3.exit, font = 'Arial 20 bold', bg= 'Red',
         fg = 'White')
  # ----------------------------------------------------------------------------
  win3.loop()
# ==============================================================================
def config(rows=24, cols=36,goals=12):
  """Creates the config window and packs the widgets"""
  global win
  win = Win(title = 'Config', op=2, grow=True) #Config window
  # ----------------------------------------------------------------------------
  font2 = 'Arial 20 bold'

  Label(win, text='CONFIGURATION',width= 23,bg='Black',fg='White',font=font2)
  # ----------------------------------------------------------------------------
  frame = Frame(win, fold = 2, flow='ES')

  Label(frame, text='Name of player A :', width=13, anchor='SW', grow=True)
  win.p1 = Entry(frame)

  Label(frame, text='Name of player B :', width=13, anchor='SW', grow=True)
  win.p2 = Entry(frame)

  Label(frame, text='Number of rows :', width=13, anchor='SW', grow=False)
  win.rowscale = Scale(frame, scale=(12,rows), flow='W', state=12)
  
  Label(frame, text='Number of cols :', width=13, anchor='SW', grow=False)
  win.colscale = Scale(frame, scale=(12,cols), flow='W', state=12)
  
  Label(frame, text='Number of goals: ', width=13, anchor='SW', grow=False)
  win.goalscale = Scale(frame, scale=(1,goals), flow='W', state=1)
  # ----------------------------------------------------------------------------
  Button(win,text='START',command=effet_config,bg='Black',fg='White',font=font2)
  # ----------------------------------------------------------------------------
  win.loop()
# ==============================================================================  
if __name__ == "__main__":
  config()
# ==============================================================================
