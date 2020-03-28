import pygame
class display:
	def __init__(self,data,screen):
		self.data=data
		self.screen =screen
		self.numOfPeople=data['game_info']['numOfPeople']

		self.font='ipamjm.ttf'
		self.font1 = pygame.font.Font(self.font, 10)
		self.font1_5 = pygame.font.Font(self.font, 15)
		self.font2 = pygame.font.Font(self.font, 20)
		self.font3=pygame.font.Font(self.font, 30)
		self.font4=pygame.font.Font(self.font, 40)
		self.font5=pygame.font.Font(self.font, 50)
		self.initialize()
	def draw_select_kyoku_button(self,i,choice=False):
		font_size=self.kyoku_select_button_font_size
		font=pygame.font.Font(self.font, font_size)
		rect=self.kyoku_select_buttons[i]
		if choice:
			flame_color=pygame.Color('green')
			body_color=pygame.Color('white')
			letter_color=pygame.Color('black')
		else:
			flame_color=pygame.Color('white')
			body_color=pygame.Color('black')
			letter_color=pygame.Color('white')
		pygame.draw.rect(self.screen, body_color, rect)
		pygame.draw.rect(self.screen, flame_color, rect,3)

		#表示テキスト
		kyoku_info=self.data['kyoku'][i]['kyoku_info']
		kyoku=kyoku_info['kyoku']
		honba=kyoku_info['honba']
		parent=kyoku_info['parent']
		wind='東 ' if kyoku<=self.numOfPeople else '南 '
		text1=wind+str((kyoku-1)%self.numOfPeople+1)+'局　'+str(honba)+'本場　親:'+str(parent)

		kyoku_end_info=self.data['kyoku'][i]['kyoku_end_info']
		frag=kyoku_end_info['frag']
		if frag=='RYUKYOKU':
			text2='流局'
		else:
			agari_info=kyoku_end_info['agari_info']
			player_id=agari_info['player_id']
			typ='ロン' if agari_info['type']=='ron' else 'ツモ'
			daten=agari_info['daten']
			text2=typ+':'+str(player_id)+'　'+str(daten)
			if typ=='ロン':
				from_player_id=agari_info['from_player_id']
				text2+='　放銃:'+str(from_player_id)
		#表示
		x,y,dx,dy=rect
		self.screen.blit(font.render(text1, True, letter_color), (x+5,y+3))
		self.screen.blit(font.render(text2, True, letter_color), (x+5,y+3+font_size))

	def initialize(self):
		self.screen.fill((0,180,0),(0,0,750,750))# 画面を緑色で塗りつぶす
			#drawの部分
		self.screen.fill((255,255,0),(750,0,350,750))# 山との間を塗りつぶす
			#button部分
		self.screen.fill((0,180,0),(1100,0,300,750))# 山部分を塗りつぶす
			#environment
		
		#ゲーム種類の表示
		self.numOfTonpu=self.data['game_info']['numOfTonpu']
		if self.numOfTonpu==1:
			typ='東風戦'
		elif self.numOfTonpu==2:
			typ='半荘戦'
		self.screen.blit(self.font5.render(typ, True, pygame.Color('black')), (850,20))
		
		#ボタンの配置
		self.button_next = pygame.Rect(760, 10, 70, 70)
		self.button_back = pygame.Rect(1020, 10, 70, 70)
		pygame.draw.rect(self.screen, pygame.Color('black'), self.button_back)
		pygame.draw.rect(self.screen, pygame.Color('black'), self.button_next)
		self.screen.blit(self.font5.render('＜', True, pygame.Color('white')), (770,20))
		self.screen.blit(self.font5.render('＞', True, pygame.Color('white')), (1030,20))
		
		#局select_uttonの配置
		self.numOfKyoku=len(self.data['kyoku'])
		rect_height=47
		self.kyoku_select_button_font_size=20
		start_y=100
		if self.numOfKyoku>13:
			rect_height=650/self.numOfKyoku-3
			self.kyoku_select_button_font_size=(rect_height-3)/2
		
		self.kyoku_select_buttons=[]	
		for i in range(self.numOfKyoku):
			rect=pygame.Rect(755, start_y+(rect_height+1)*i,340,rect_height)
			self.kyoku_select_buttons.append(rect)
			self.draw_select_kyoku_button(i)
		
		#一曲目の開始
		self.current_kyoku=0
		self.setting_kyoku(0)
	def setting_kyoku(self,i):
		self.draw_select_kyoku_button(self.current_kyoku)
		self.current_kyoku=i 
		self.draw_select_kyoku_button(i,choice=True)
		#卓の設定
		pass
	def back(self):
		pass
	def next(self):
		pass
	def button_controll(self,pos):
		if self.button_next.collidepoint(pos):
			self.next()
		elif self.button_back.collidepoint(pos):
			self.back()
		else:
			for i in range(self.numOfKyoku):
				if self.kyoku_select_buttons[i].collidepoint(pos):
					self.setting_kyoku(i)
					break
			else:
				return False
		return True
