import pygame
import numpy as np
import library_replay as lib
class controller:
	def __init__(self,data,screen,taku,draw):
		self.data=data
		self.screen =screen
		self.taku=taku
		self.draw=draw
		self.numOfPeople=self.taku.numOfPeople
		self.font='ipamjm.ttf'
		self.font1 = pygame.font.Font(self.font, 10)
		self.font1_5 = pygame.font.Font(self.font, 15)
		self.font2 = pygame.font.Font(self.font, 20)
		self.font2_5 = pygame.font.Font(self.font, 25)
		self.font3=pygame.font.Font(self.font, 30)
		self.font4=pygame.font.Font(self.font, 40)
		self.font5=pygame.font.Font(self.font, 50)
		self.current_kyoku=0
		self.current_index=0
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

		#kyokuは3人も4人もどちらも
		wind=['東','南','西','北'][(kyoku-1)//self.numOfPeople]
		text1=wind+str((kyoku-1)%self.numOfPeople+1)+'局　'+str(honba)+'本場　親:'+str(parent)

		kyoku_end_info=self.data['kyoku'][i]['kyoku_end_info']
		type=kyoku_end_info['type']
		if type=='RYUKYOKU':
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
	def draw_controll_button(self):
		self.button_back = lib.controll_button((760, 10, 70, 70),'＜',self.screen)
		self.button_next = lib.controll_button((1020, 10, 70, 70),'＞',self.screen)

	def initialize(self):
		self.screen.fill((0,180,0),(0,0,750,750))# 画面を緑色で塗りつぶす
			#drawの部分
		self.screen.fill((255,255,0),(750,0,350,750))# 山との間を塗りつぶす
			#button部分
		self.screen.fill((0,180,0),(1100,0,300,750))# 山部分を塗りつぶす
			#environment
		

		#ゲームルールのルールの表示
		if 'rule' in self.data['game_info'].keys():
			self.rule=self.data['game_info']['rule']
			rule='ルール： '
			if self.rule=='tenho':
				rule+='天鳳'+str(self.numOfPeople)+'人打'
			self.screen.blit(self.font2.render(rule, True, pygame.Color('black')), (840,10))
		#ゲーム種類の表示
		self.numOfTonpu=self.taku.numOfTonpu
		if self.numOfTonpu==1:
			typ='東風戦'
		elif self.numOfTonpu==2:
			typ='半荘戦'
		self.screen.blit(self.font2.render(typ, True, pygame.Color('black')), (895,50))
		#終局結果の表示
		x=1105
		y=5
		dx=290
		dy=220
		normal_font_size=25
		normal_font=pygame.font.Font(self.font, normal_font_size)
		rect=pygame.Rect(x,y,dx,dy)
		pygame.draw.rect(self.screen, pygame.Color('gray'), rect)#body_rect
		pygame.draw.rect(self.screen, pygame.Color('blue'), rect,3)#flame_rect
			#text
		score=self.data['game_end_info']['score']
		s=[score[2*i] for i in range(self.numOfPeople)]
		args=np.argsort(s)[::-1]
		for i in range(self.numOfPeople):
			ddx,ddy=x+5,y+3+i*normal_font_size*2+2
			text=''
			j=args[i]
			text+=str(i+1)+'位: '+self.taku.janshi[j].name
			self.screen.blit(normal_font.render(text, True,pygame.Color('black')), (ddx,ddy))

			s1='{:>5}'.format(int(score[2*j])*100)
			s2=score[2*j+1]
			if float(s2)>0:
				s2=f'+{s2}'
			text=f' {s1}  ({s2})'
			self.screen.blit(normal_font.render(text, True,pygame.Color('black')), (ddx+2*normal_font_size,ddy+normal_font_size))

		#局select_uttonの配置
		self.numOfKyoku=len(self.data['kyoku'])
		rect_height=47
		self.kyoku_select_button_font_size=20
		start_y=100
		if self.numOfKyoku>13:
			rect_height=600/self.numOfKyoku-3
			self.kyoku_select_button_font_size=(rect_height-3)/2
		
		self.kyoku_select_buttons=[]	
		for i in range(self.numOfKyoku):
			rect=pygame.Rect(755, start_y+(rect_height+1)*i,340,rect_height)
			self.kyoku_select_buttons.append(rect)
			self.draw_select_kyoku_button(i)
		#コントロールボタンの配置
		self.draw_controll_button()

		#一曲目の開始
		self.current_kyoku=0
		self.setting_kyoku(0)

		self.draw.initialize()
	def setting_kyoku(self,i):
		if i<0 or i>=self.numOfKyoku:
			return 0
		self.draw_select_kyoku_button(self.current_kyoku)
		self.current_kyoku=i
		self.draw_select_kyoku_button(i,choice=True)
		self.taku.setting_kyoku(i)
		self.current_index=-1
		self.length_index=len(self.data['kyoku'][self.current_kyoku]['moda'])
		self.draw.kyoku_start()
		self.draw.draw_taku()

		self.after_naki=False
		self.kyoku_end=False
	def back(self):
		if self.current_index==0:
			self.setting_kyoku(self.current_kyoku-1)
		else:
			self.current_index-=1
			data=self.data['kyoku'][self.current_kyoku]['moda'][self.current_index]
			self.taku.back(data)
			self.draw.draw_taku()
	def next(self):
		if self.kyoku_end:
			self.kyoku_end=False
			self.setting_kyoku(self.current_kyoku+1)
		elif self.current_index==self.length_index-1:
			self.current_index+=1#一応+1してるよー
			self.kyoku_end=True
			data=self.data['kyoku'][self.current_kyoku]['kyoku_end_info']
			self.draw.draw_kyoku_end(data)
		elif self.after_naki:
			self.after_naki=False
			self.draw.draw_taku()
		else:
			self.current_index+=1
			data=self.data['kyoku'][self.current_kyoku]['moda'][self.current_index]
			if data['type']=='TSUMO':
				self.taku.next(data)
				player_id=data['player_id']
				self.draw.draw_taku(tsumo_id=player_id)
			elif data['type']=='DAHAI':
				self.taku.next(data)
				player_id=data['player_id']
				self.draw.draw_taku(dahai_id=player_id)
			elif data['type']=='REACH':
				if data['step']==1:
					player_id=data['player_id']
					self.taku.next(data)
					self.draw.draw_speaking(player_id,'REACH')
				else:
					self.taku.next(data)
					self.draw.draw_taku()
			elif data['type']=='NAKI':
				self.after_naki=True
				player_id=data['player_id']
				self.taku.next(data)
				self.draw.draw_speaking(player_id,data['type2'])
			elif data['type']=='AGARI':
				player_id=data['player_id']
				self.draw.draw_speaking(player_id,data['type2'])
			elif data['type']=='DORA':
				self.taku.next(data)
				self.draw.draw_taku()
			elif data['type']=='RYUKYOKU':
				self.draw.draw_ryukyoku()
	def mouse_button_down(self,pos):
		if self.button_next.button_down(pos) or self.button_back.button_down(pos):
			return True
		else:
			for i in range(self.numOfKyoku):
				if self.kyoku_select_buttons[i].collidepoint(pos):
					self.setting_kyoku(i)
					break
			else:
				return False
		return True
	def mouse_button_up(self):
		if self.button_back.button_up() :
			self.back()
		elif self.button_next.button_up():
			self.next()
		else:
			return False
		return True

	