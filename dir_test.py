from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label

def direction(pos_ini,pos_end):
  dx = pos_end[0]-pos_ini[0]
  dy = pos_end[1]-pos_ini[1]
  if dx>=0 and dx>= abs(dy):
    direc=1
  elif dy>=0 and dy>=abs(dx):
    direc=2
  elif dx<0 and abs(dx)>=abs(dy):
    direc=-1
  elif dy<0 and abs(dy)>=abs(dx):
    direc=-2
  return direc

class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.labeltext = 'direction:'
    self.label = Label(text=self.labeltext)
    self.add_widget(self.label)

  def on_touch_down(self, touch): 
    self.pos_ini =(touch.x, touch.y)
    #touch.ud['dir'] = pos_ini 
  
  def on_touch_up(self, touch): 
    self.pos_end = (touch.x, touch.y)
    direc = direction(self.pos_ini,self.pos_end)
    self.labeltext = 'direction: '+str(direc)
    self.label.text = self.labeltext

class DirTestApp(App):
  def build(self):
    game = MyWidget()
    return game

if __name__ == '__main__':
  DirTestApp().run()
