import pyglet
from pyglet.window import key, FPSDisplay
from pyglet.sprite import Sprite

from GameObjects import GameObject, preload_image

class GameWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super(GameWindow, self).__init__(*args, **kwargs)
		self.set_location(400,100)
		self.frame_rate = 1/60.0
		self.fps_display = FPSDisplay(self)
		self.fps_display.label.font_size = 50
		self.fps_display.label.y = 300

		self.right = False
		self.left = False
		self.player_speed = 300 
		self.fire = False
		self.player_fire_rate = 0

		player_spr = pyglet.sprite.Sprite(preload_image('Carrot.png'))
		self.player = GameObject(500, 100, 0, 0, player_spr)

		self.player_laser = preload_image('laser.png')
		self.player_laser_list = []
		

		self.grass_list = []
		self.grass_img = preload_image('Grass.png')
		for i in range(3):
			self.grass_list.append(GameObject(0, i*675, 0, -200, Sprite(self.grass_img)))

	def on_key_press(self, symbol, modifiers):
		if symbol == key.RIGHT:
			self.right = True
		if symbol == key.LEFT:
			self.left = True
		if symbol == key.SPACE:
			self.fire = True
			#self.player_laser_list.append(GameObject(self.player.posx, self.player.posy, 0, 0, Sprite(self.player_laser)))
		if symbol == key.ESCAPE:
			pyglet.app.exit()

	def on_key_release(self, symbol, modifiers):
		if symbol == key.RIGHT:
			self.right = False
		if symbol == key.LEFT:
			self.left = False
		if symbol == key.SPACE:
			self.fire = False
	def on_draw(self):
		self.clear()
		for grass in self.grass_list:
			grass.draw()
		self.player.draw()
		for lsr in self.player_laser_list:
			lsr.draw()
		self.fps_display.draw()


	def update_player(self,dt):
		self.player.update(dt)
		if self.right and self.player.posx < 1000 - self.player.width:
			self.player.posx += self.player_speed * dt
		if self.left and self.player.posx > 100:
			self.player.posx -= self.player_speed * dt

	def update_player_laser(self,dt):
		for lsr in self.player_laser_list:
			lsr.update(dt)
			lsr.posy += 400 * dt
			if lsr.posy > 700:
				self.player_laser_list.remove(lsr)

	def player_fire(self,dt):
		self.player_fire_rate -= dt
		if self.player_fire_rate <=0:	
			self.player_laser_list.append(GameObject(self.player.posx, self.player.posy + 76, 0, 0, Sprite(self.player_laser)))
			self.player_fire_rate += 0.2
			
	
	def update_space(self,dt):
		first_grass = self.grass_list[0]
		if first_grass.posy <= -975:
			first_grass = self.grass_list.pop(0)
			last_grass = self.grass_list[-1]
			first_grass.posy = last_grass.posy + 675
			self.grass_list.append(first_grass)

		# positions = ""
		for grass in self.grass_list:
			grass.update(dt)
			# positions += grass.posy
			#grass.posy -=50

	def update(self, dt):
		self.update_player(dt)
		if self.fire:
			self.player_fire(dt)

		self.update_player_laser(dt)
		self.update_space(dt)

		
		

if __name__ =="__main__":
	window = GameWindow(1200,675,"Veggie Invaders", resizable=False)
	pyglet.clock.schedule_interval(window.update, window.frame_rate)
	pyglet.app.run()
