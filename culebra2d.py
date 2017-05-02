from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import Ellipse, Rectangle
from kivy.graphics import Color
from kivy.clock import Clock

import random 

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
	
class SnakeBall(Ellipse):
	def __init__(self,**kwargs):
		super(SnakeBall,self).__init__(**kwargs)
	def update(self,pose):
		self.pos = pose
		
class SnakeHead(SnakeBall):
	def __init__(self,**kwargs):
		super(SnakeHead,self).__init__(**kwargs)

	def update(self,mypose):
		super(SnakeHead,self).update(mypose)
		
class SnakeBody(SnakeBall):
	def __init__(self,**kwargs):
		super(SnakeBody,self).__init__(**kwargs)
	def update(self,mypose):
		super(SnakeBody,self).update(mypose)

class Food(Ellipse):
	def __init__(self,**kwargs):
		super(Food,self).__init__(**kwargs)
	def update(self,mypose):
		super(Food,self).update(mypose)

class Score(Label):	
	def __init__(self,**kwargs):
		super(Score,self).__init__(**kwargs)
	
	def update(self,*ignore):
		self.text = self.parent.textscore
		
class Game(Widget):
	def __init__(self):
		super(Game, self).__init__()
		self.score = 0
		self.direction = 0
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		
		self.size = (640,600)
		self.mylayout = 10
		height_unit = int(self.height / self.mylayout)
		self.textscore = text = 'score: '+str(self.score)
		self.score_label = Score(text=self.textscore)
		self.add_widget(self.score_label)
		self.score_label.height = 2*height_unit
		#self.score_label.width = self.width
		self.score_label.y = 8 * height_unit
		self.background = Background(source='background.png')
		self.add_widget(self.background)
		self.background.height = 8*height_unit
		self.background.width = self.width
		self.background.y = self.y
		
		self.snake = []
		self.snake_size = 3
		self.grid = (16,12)
		color_head = [0,0,1.0]
		color_snake = [0.3,0.3,0.5]
		color_food = [1.0,0.2,0.2]
		(self.width_grid,self.height_grid) = (int(self.background.width/self.grid[0]),int(self.background.height/self.grid[1]))
		mysize = (self.width_grid,self.height_grid)
		with self.canvas:
			Color(*color_head)
			self.snake_poses = []
			self.snake_poses.append([self.grid[0]/2,self.grid[1]/2])
			position = self.get_position(self.snake_poses[-1])
			self.snake.append(SnakeHead(pos=position,size=mysize))
			Color(*color_snake)
			for i in range(self.snake_size-1):
				self.snake_poses.append([self.grid[0]/2-i-1,self.grid[1]/2])
				position = (self.width_grid*self.snake_poses[-1][0],self.height_grid*self.snake_poses[-1][1])
				self.snake.append(SnakeBall(pos=position,size=mysize))
			self.snake_to_move = self.snake_size-1
			Color(*color_food)
			self.food_pos = (random.randint(0,self.grid[0]),random.randint(0,self.grid[1]))
			position = self.get_position(self.food_pos)
			self.food = Food(pos=position,size=mysize)

			Clock.schedule_interval(self.update, 1.0/2.0)		

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'left':
			self.direction = -1 
		elif keycode[1] == 'right':
			self.direction = 1
		elif keycode[1] == 'up':
			self.direction = 2
		elif keycode[1] == 'down':
			self.direction = -2
		return True

	def on_touch_down(self, touch): 
		self.pos_ini =(touch.x, touch.y)
		#touch.ud['dir'] = pos_ini 
  
	def on_touch_up(self, touch): 
		self.pos_end = (touch.x, touch.y)
		direc = direction(self.pos_ini,self.pos_end)
		self.direction = direc

	def get_position(self, pose):
		'''
		dada la posicion matricial pose devuelve la posicion de la pantalla de acuerdo
		a la grilla
		'''
		return (self.width_grid*(pose[0]),self.height_grid*(pose[1]))
		
	def update(self,*ignore):
		if self.direction != 0:
			old_head_pose = self.snake_poses[0]
			if self.direction == -1:
				self.snake_poses[0][0] -= 1  
			elif self.direction == 1:
				self.snake_poses[0][0] += 1  
			elif self.direction == 2:
				self.snake_poses[0][1] += 1  
			elif self.direction == -2:
				self.snake_poses[0][1] -= 1 
			#self.textscore = "score: " + str(self.score)
			#self.score_label.update()
			position = self.get_position(self.snake_poses[0])
			self.snake[0].update(position)
			self.snake_poses[self.snake_to_move] = old_head_pose
			position = self.get_position(old_head_pose)
			self.snake[self.snake_to_move].update(position)		
			if self.snake_to_move == self.snake_size-1:
				self.snake_to_move = 1
			else:
				self.snake_to_move += 1


class Culebra2DApp(App):
	def build(self):
		game = Game()
		Window.size = game.size
		return game

if __name__ == "__main__":
	Culebra2DApp().run()