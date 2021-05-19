import pygame
class controll_button:
	def __init__(self,rect,text,screen):
		self.text=text
		self.rect=pygame.Rect(rect)
		self.x,self.y,self.dx,self.dy=rect
		self.font_name='ipamjm.ttf'
		self.screen=screen
		self.frame_width=3
		self.font=pygame.font.Font(self.font_name,50)
		self.set_nonactive()
		self.draw()
		
	def set_active(self):
		self.active=True
		self.color=pygame.Color('white')
		self.frame_color=pygame.Color('green')
		self.font_color=pygame.Color('black')
	def set_nonactive(self):
		self.active=False
		self.color=pygame.Color('black')
		self.frame_color=pygame.Color('white')
		self.font_color=pygame.Color('white')
	def button_down(self,pos):
		if self.rect.collidepoint(pos):
			self.set_active()
			self.draw()
			return True
		else:
			return False
	def button_up(self):
		if self.active:
			self.set_nonactive()
			self.draw()
			return True
		else:
			return False
	def draw(self):
		pygame.draw.rect(self.screen, self.color, self.rect)
		pygame.draw.rect(self.screen, self.frame_color, self.rect,self.frame_width)
		self.screen.blit(self.font.render(self.text, True, self.font_color),(self.x+10,self.y+10))
