import pygame
class draw:
	def __init__(self,taku,screen):
			fo='ipamjm.ttf'
			self.run=True
			self.screen=screen
			self.taku=taku
			self.font1 = pygame.font.Font(fo, 10)
			self.font1_5 = pygame.font.Font(fo, 15)
			self.font2 = pygame.font.Font(fo, 20)
			self.font3=pygame.font.Font(fo, 30)
			self.font4=pygame.font.Font(fo, 40)
			self.font5=pygame.font.Font(fo, 50)
			tumibo=pygame.transform.smoothscale(pygame.image.load('image/tennbou-100.jpg').convert(),(10,100))
			self.tumibo=pygame.transform.rotate(tumibo,90)
			richibo=pygame.transform.smoothscale(pygame.image.load('image/tennbou-1000.jpg').convert(),(10,100))
			self.richibo=pygame.transform.rotate(richibo,90)
			self.back_color_of_pai=(255,190,0)
			
	def draw_center_info(self):
		pass
	def draw_tehai(self,i):
		pass
	def draw_kawa(self,i):
		pass
	def draw_chicha_mark(self):
		pass
	def draw_naki(self):
		pass
	def draw_kyoku_end(self):
		pass
	def draw_game_end(self):
		pass
	