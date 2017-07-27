from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import Ellipse, Rectangle
from kivy.graphics import Color
from kivy.clock import Clock

import random 
import os

GAME_SPEED = 4

def direction(pos_ini,pos_end):
  '''
  define la direccion dadas las diferencias entre las posiciones iniciales y finales
  del movimiento touch. right=1 left=-1 up=2 down=-2
  '''
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
  
class Background(Image):
  def __init__(self,**kwargs):
    super(Background,self).__init__(**kwargs)
    self.allow_stretch = True
    self.keep_ratio = False
  
class Ball(Ellipse):
  def __init__(self,**kwargs):
    super(Ball,self).__init__(**kwargs)
  def update(self,pose):
    self.pos = pose
    
'''   
class SnakeHead(SnakeBall):
  def __init__(self,**kwargs):
    super(SnakeHead,self).__init__(**kwargs)

  def update(self,pose):
    super(SnakeHead,self).update(pose)
    
class SnakeBody(SnakeBall):
  def __init__(self,**kwargs):
    super(SnakeBody,self).__init__(**kwargs)
  def update(self,pose):
    super(SnakeBody,self).update(pose)

class Food(Ellipse):
  def __init__(self,**kwargs):
    super(Food,self).__init__(**kwargs)
  def update(self,pose):
    super(Food,self).update(pose)
'''
class Score(Button): 
  def __init__(self,**kwargs):
    super(Score,self).__init__(**kwargs)
    
  def update(self,*ignore):
    self.text = self.parent.textscore
    #self.x = 0

  def _on_press(self,event):
    print('callback called')
    self.text = 'touched!' + self.parent.textscore 
    self.parent.game.pause()
    
class Game(Widget):
  def __init__(self, **kwargs):
    super(Game, self).__init__(**kwargs)
    self.pos_ini = (0,0)
    if os.name == 'nt':
      self.size = (600,600)
    elif os.name == 'posix':
      self.size = Window.size
    self.user = 'danomax'
    self.score = 0
    self.direction = 0
    self.velocity = GAME_SPEED
    self.paused = True
    self.grid = (16,12)
    self.textscore = text = 'score: '+str(self.score)
    self.score_label = Score(text=self.textscore, halign='center')
    #self.score_label.bind(on_press=self.score_label._on_press)
    self.score_label.bind(on_press=self.callback)
    self.background = Background(source='background.png')
    self.resize()
    if os.name == 'nt':
      self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
      self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self.add_widget(self.score_label)
    self.add_widget(self.background)
    self.snake = []         #objetos de la culebra
    self.snake_size = 3
    self.grid_snake = []    #mantiene una matriz que es true en las celdas ocupadas por la culebra
    self.snake_poses = []   #lista de posiciones de la culebra
    self.snake_mask_colors = [0.0, 1.0, 0.0]  #Mascara de colores de la culebra
    for i in range(self.grid[0]):
      self.grid_snake.append([])
      for j in range(self.grid[1]):
        self.grid_snake[i].append(False)
    self.Draw()
    Clock.schedule_interval(self.update, 1.0/self.velocity)     

  def Draw(self):
    with self.canvas:
      color_random = [random.random(),random.random(),random.random()]
      color_snake = [x*y for x,y in zip(color_random,self.snake_mask_colors)]+[1]
      Color(*color_snake)
      (x,y) = (int(self.grid[0]/2),int(self.grid[1]/2))
      self.snake_poses.append([x,y])
      self.grid_snake[x][y] = True
      position = self.get_position(self.snake_poses[0])
      self.snake.append(Ball(pos=position,size=self.ballsize))
      for i in range(1,self.snake_size):
        color_random = [random.random(),random.random(),random.random()]
        color_snake = [x*y for x,y in zip(color_random,self.snake_mask_colors)]+[1]
        Color(*color_snake)
        (x,y) = (int(self.grid[0]/2-i),int(self.grid[1]/2))
        self.snake_poses.append([x,y])
        self.grid_snake[x][y] = True
        position = self.get_position(self.snake_poses[-1])
        self.snake.append(Ball(pos=position,size=self.ballsize))
      self.snake_to_move = self.snake_size-1
      color_food = [1.0,0.2,0.2]
      Color(*color_food)
      self.food_pos = (random.randint(1,self.grid[0]),random.randint(1,self.grid[1]))
      self.food_pos = self.new_food_pos()
      position = self.get_position(self.food_pos)
      self.food = Ball(pos=position,size=self.ballsize)

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left' and self.direction != 1:
      self.direction = -1 
    elif keycode[1] == 'right' and self.direction != -1:
      self.direction = 1
    elif keycode[1] == 'up' and self.direction != -2:
      self.direction = 2
    elif keycode[1] == 'down' and self.direction != 2:
      self.direction = -2
    if self.paused: self.pause()
    elif keycode[1] == 'p':
      self.pause()
    return True
  '''
  def on_touch_down(self, touch): 
    if touch.y < self.background.height:
      self.pos_ini =(touch.x, touch.y)
  
  def on_touch_up(self, touch): 
    if touch.y < self.background.height:
      self.pos_end = (touch.x, touch.y)
      direc = direction(self.pos_ini,self.pos_end)
      if self.direction != -direc:
        self.direction = direc
  '''
  def callback(self,event):
    print('callback called')
    self.text = 'touched!' + self.textscore 
    self.pause()

  def resize(self):
    self.score_label.size = self.width, 0.1*self.height
    self.score_label.y = self.height - self.score_label.height
    self.background.size = self.width, 0.9 * self.height
    self.background.y = 0 
    (self.width_grid,self.height_grid) = (int(self.background.width/self.grid[0]),int(self.background.height/self.grid[1]))
    self.ballsize = (self.width_grid,self.height_grid)
    self.update()


  def get_position(self, pose):
    '''
    dada la posicion matricial pose devuelve la posicion de la pantalla de acuerdo
    a la grilla
    '''
    return (self.width_grid*(pose[0]),self.height_grid*(pose[1]))

  def new_food_pos(self):
    '''
    retorna nueva posicion para la comida luego de ser devorada
    '''
    #encontra el numero de espacios libres en la grilla
    empty_spaces = self.grid[0]*self.grid[1]
    empty_spaces = empty_spaces - self.snake_size
    #escoge el numero aleatorio entre 1 y empty_spaces
    choose_num = random.randint(1,empty_spaces)
    #encuentra el espacio evitando los espacios ocupados por la culebra
    num=0
    for i in range(self.grid[0]):
      for j in range(self.grid[1]):
        if self.grid_snake[i][j]==False:
          num+=1
        if num == choose_num:
          return (i,j)
    #si no encuentra espacio, se lleno la grilla de culebra, fin del juego!
    return (-1,-1)

  def game_over(self):
    filename = 'bests.hsc'
    max_scores = 10
    with open(filename) as f:
      seq = f.readlines()
    i=0
    z=''
    Recorded = False
    if seq != []:
      for s in seq:
        data = s.strip().split(',')
        if self.score > int(data[2]) and not Recorded:
          z += str(i)+','+self.user+',' + str(self.score) + '\n'
          i+=1
          Recorded = True  
        if i<max_scores:
          z += str(i) + ',' + data[1] + ',' + data[2] + '\n'
          i +=1
    if i<max_scores:
      if not Recorded:
        z += str(i)+','+self.user+',' + str(self.score) + '\n'
 
    with open(filename,'w') as f:
      f.write(z)
    self.clear_widgets()
    Clock.unschedule(self.update)
    self.__init__()

  def update(self,*ignore):
    #actualiza la posicion de la cabeza de acuerdo a la direccion
    if self.direction != 0:
      old_head_pose = (self.snake_poses[0][0],self.snake_poses[0][1])
      if self.direction == -1:
        if self.snake_poses[0][0] > 0:
          self.snake_poses[0][0] -= 1 
        else:
          self.game_over()
          return
      elif self.direction == 1:
        if self.snake_poses[0][0] < self.grid[0]-1:
          self.snake_poses[0][0] += 1 
        else:
          self.game_over()
          return
      elif self.direction == 2:
        if self.snake_poses[0][1] < self.grid[1]-1:
           self.snake_poses[0][1] += 1
        else:
           self.game_over()
           return
      elif self.direction == -2:
        if self.snake_poses[0][1] > 0:
          self.snake_poses[0][1] -= 1
        else:
          self.game_over()
          return
      #chequear si ha chocado consigo misma
      if self.grid_snake[self.snake_poses[0][0]][self.snake_poses[0][1]]:
        self.game_over()
        return
      else:
        #actualiza la grilla grid_snake con la nueva posicion
        self.grid_snake[self.snake_poses[0][0]][self.snake_poses[0][1]] = True
        position = self.get_position(self.snake_poses[0])
        self.snake[0].update(pose=position)

      if self.snake_poses[0][0] == self.food_pos[0] and self.snake_poses[0][1] == self.food_pos[1]:
        #Se come el alimento
        self.score += 100
        old_pose = (old_head_pose[0],old_head_pose[1])
        if self.snake_to_move == self.snake_size-1: 
          #La culebra esta ordenada, recorrer desde 1 hasta el snake_size - 1:
          for a in range(1,self.snake_to_move+1):
            temp_pose = (self.snake_poses[a][0],self.snake_poses[a][1])
            self.snake_poses[a] = (old_pose[0],old_pose[1])
            position = self.get_position(self.snake_poses[a])
            self.snake[a].update(position)
            old_pose = (temp_pose[0],temp_pose[1])
          self.snake_to_move += 1
        else:
          #La culebra esta desordenada, recorrer desde snake_to_move+1 hasta snake_size-1
          for a in range(self.snake_to_move+1,self.snake_size):
            temp_pose = (self.snake_poses[a][0],self.snake_poses[a][1])
            self.snake_poses[a] = (old_pose[0],old_pose[1])
            position = self.get_position(self.snake_poses[a])
            self.snake[a].update(position)
            old_pose = (temp_pose[0],temp_pose[1])     
        self.snake_poses.append(old_pose)
        self.snake_size += 1
        with self.canvas:
          color_random = [random.random(),random.random(),random.random()]
          color_snake = [x*y for x,y in zip(color_random,self.snake_mask_colors)]+[1]
          Color(*color_snake)
          position = self.get_position(old_pose)
          mysize = (self.width_grid,self.height_grid)
          self.snake.append(Ball(pos = position, size = mysize))
        #self.food_pos = (random.randint(1,self.grid[0]),random.randint(1,self.grid[1]))
        self.food_pos = self.new_food_pos()
        position = self.get_position(self.food_pos)
        self.food.update(pose=position)
      else:
        self.grid_snake[self.snake_poses[self.snake_to_move][0]][self.snake_poses[self.snake_to_move][1]] = False
        self.snake_poses[self.snake_to_move] = (old_head_pose[0],old_head_pose[1])
        position = self.get_position(old_head_pose)
        self.snake[self.snake_to_move].update(pose=position)    
        if self.snake_to_move == 1:
          self.snake_to_move = self.snake_size-1
        else:
          self.snake_to_move -= 1
      self.textscore = "score: " + str(self.score)
      self.score_label.x = self.x
      self.score_label.update()

  def pause(self):
    if not self.paused:
      Clock.unschedule(self.update)
      self.paused = True
    else:
      Clock.schedule_interval(self.update,1/self.velocity)
      self.paused = False

class Culebra2DApp(App):
  def build(self):
    game = Game()
    if os.name == 'nt':
      Window.size = game.size
    return game

  def on_resize(self):
    game.resize()

if __name__ == "__main__":
  Culebra2DApp().run()