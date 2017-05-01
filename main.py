from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import Ellipse, Rectangle
from kivy.graphics import Color
from kivy.clock import Clock

import random 
	
class Background(Image):
	def __init__(self,**kwargs):
		super(Background,self).__init__(**kwargs)
		self.allow_stretch = True
		self.keep_ratio = False
	
class SnakeBall(Ellipse):
	def __init__(self,**kwargs):
		super(SnakeBall,self).__init__(**kwargs)
		
class SnakeHead(SnakeBall):
	def __init__(self,**kwargs):
		super(SnakeHead,self).__init__(**kwargs)

class SnakeBody(SnakeBall):
	def __init__(self,**kwargs):
		super(SnakeBody,self).__init__(**kwargs)

class Food(Ellipse):
	def __init__(self,**kwargs):
		super(Food,self).__init__(**kwargs)
		
		
class Game(Widget):
	def __init__(self):
		super(Game, self).__init__()
		self.score = 0
		self.size = (320,300)
		self.mylayout = 10
		height_unit = int(self.height / self.mylayout)
		self.score_label = Label(text = 'score: '+str(self.score))
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
		color_food = Color([1.0,0.2,0.2])
		(self.width_grid,self.height_grid) = (int(self.background.width/self.grid[0]),int(self.background.height/self.grid[1]))
		with self.canvas:
			Color(*color_head)
			position = (self.width_grid*(self.grid[0]/2),self.height_grid*(self.grid[1]/2))
			mysize = (self.width_grid,self.height_grid)
			self.snake.append(SnakeHead(pos=position,size=mysize))
			Color(*color_snake)
			for i in range(self.snake_size-1):
				position = (self.width_grid*(self.grid[0]/2-i-1),self.height_grid*(self.grid[1]/2))
				self.snake.append(SnakeBall(pos=position,size=mysize))
			#color = color_food
			#food_pos = (random.randint(0,self.grid[0]),random.randint(0,self.grid[1]))
			#self.food = Food(pos=food_pos,size=(self.width_grid/2,self.height_grid/2))
		
		Clock.schedule_interval(self.update, 1.0/60.0)
		
		
		
	def update(self,*ignore):
		pass


class Culebra2DApp(App):
	def build(self):
		game = Game()
		Window.size = game.size
		return game

if __name__ == "__main__":
	Culebra2DApp().run()
