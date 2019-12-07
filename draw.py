import pygame
class draw_controll:
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
			tumibo=pygame.transform.smoothscale(pygame.image.load('image/tennbou-100.jpg').convert(),(10,100))
			self.tumibo=pygame.transform.rotate(tumibo,90)
			richibo=pygame.transform.smoothscale(pygame.image.load('image/tennbou-1000.jpg').convert(),(10,100))
			self.richibo=pygame.transform.rotate(richibo,90)
			
			self.alpha=70
			screen.fill((0,180,0),(0,0,750,750))# 画面を緑色で塗りつぶす
			screen.fill((255,255,0),(750,0,200,750))# 山との間を塗りつぶす
			screen.fill((0,180,0),(950,0,450,750))# 山部分を塗りつぶす
			self.button_undo = pygame.Rect(760, 110, 50, 60)
			self.button_stop = pygame.Rect(825, 110, 50, 60)
			self.button_run = pygame.Rect(890, 110, 50, 60)
			self.button_new_game = pygame.Rect(770, 250, 160, 60)
			if taku.numOfKyoku==1:
				self.taku_info='一局戦'
			elif taku.numOfTonpu==1:
				self.taku_info='東風戦'
			else :
				self.taku_info='半荘戦'
			screen.blit(self.font3.render(self.taku_info, True, (0,0,0)), (770,20))
			self.state='normal'#[normal,naki,kyoku_end]
			self.naki=False
			self.naki_id=0
			self.back_color_of_pai=(255,190,0)

	def draw_yama(self,yama):
		def point(i):
			x=950
			y=121+15*34
			if i<34:
				return(x+20+40*(i%2),y-15*(i%34))
			if 34*1<=i and i<34*2:
				return(x+20+80*1+30*1+40*(i%2),y-15*(i%34))
			if 34*2<=i and i<34*3:
				return(x+20+80*2+30*2+40*(i%2),y-15*(i%34))
			if 34*3<=i and i<34*4:
				return(x+20+80*3+30*3+40*(i%2),y-15*(i%34))
		self.screen.fill((0,180,0),(950,0,450,750))
		length=len(yama.yama)
		for i in range(length):
			img=yama.yama[i].image
			img=pygame.transform.rotate(img,-90)
			self.screen.blit(img, point(i))
		#終了場所
		last_pai=length-self.taku.lastOfYama
		x,y=point(last_pai)
		self.screen.fill((255,0,190),(x,y+29,40,10))
		#表示牌
		for i in yama.dora_hyouji:
			surface=pygame.transform.rotate(pygame.Surface((29,40)),-90)
			surface.fill((255,50,255))
			surface.set_alpha(self.alpha)
			self.screen.blit(surface,point(i))
		return 1
	def draw_tehai(self,tehai,janshi_id,furo_mentsu):
		def tehai_rect(id):
			if id==0:
				return (90,660,660,90)
			elif id ==1:
				return (660,0,90,660)
			elif id ==2:
				return (0,0,660,90)
			else: 
				return (0,90,90,660)
		def point_and_direction(janshi_id):
			if janshi_id==0:
				return(90,700,29,0)
			if janshi_id==1:
				return(700,631,0,-29)
			if janshi_id==2:
				return(631,10,-29,0)
			if janshi_id==3:
				return(10,90,0,29)

		self.screen.fill((0,180,0),tehai_rect(janshi_id))
		x,y,vx,vy=point_and_direction(janshi_id)
		for i in range(len(tehai)):
			pai=tehai[i]
			img=pai.image
			img=pygame.transform.rotate(img,90*janshi_id)
			vvx,vvy=x+vx*i,y+vy*i
			if self.taku.state=='action' and i==len(tehai)-1:
				vvx,vvy=vvx+vx,vvy+vy
			self.screen.blit(img,(vvx,vvy))
			if pai in self.taku.dora:
				surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
				surface.fill((255,255,0))
				surface.set_alpha(self.alpha)
				self.screen.blit(surface,(x+vx*i,y+vy*i))
			
		#furoは左から
		def furo_point_and_direction(janshi_id):
			#(x,y,dx,dy,倒れるdx,倒れるdy、戻るdx,戻るdy)
			if janshi_id==0:
				return(671,700,-29,0,-40,11,-29,-11)
			if janshi_id==1:
				return(700,79,0,29,11,29,-11,40)
			if janshi_id==2:
				return(50,10,29,0,29,0,40,0)
			if janshi_id==3:
				return(10,671,0,-29,0,-40,0,-29)
		def draw_chi_or_pon(furo_ed_pai,ed_player_id,last_pai,janshi_id,screen,furox,furoy):
			_,_,dx,dy,rotx,roty,undox,undoy=furo_point_and_direction(janshi_id)
			x,y=furox,furoy
			if ed_player_id<janshi_id:
				d=ed_player_id-janshi_id+3
			else:d=ed_player_id-janshi_id-1
			k=1
			for i in range(3):
				if i==d:
					x-=dx
					y-=dy
					x+=rotx
					y+=roty
					pai=furo_ed_pai
					rot_id=(janshi_id+1)%4
				else:
					pai=last_pai[k]
					rot_id=janshi_id
					k=k-1
				img=pai.image
				img=pygame.transform.rotate(img,90*rot_id)
				self.screen.blit(img,(x,y))
				if pai in self.taku.dora:
					surface=pygame.transform.rotate(pygame.Surface((29,40)),90*rot_id)
					surface.fill((255,255,0))
					surface.set_alpha(self.alpha)
					screen.blit(surface,(x,y))
				
				if i==d:
					x+=undox
					y+=undoy
				else:
					x+=dx
					y+=dy
			return(x,y)
		
		def draw_ankan(furo_ed_pai,ed_player_id,last_pai,janshi_id,screen,furox,furoy):
			return (furox,furoy)
		def draw_daiminkan(furo_ed_pai,ed_player_id,last_pai,janshi_id,screen,furox,furoy):
			return (furox,furoy)
		def draw_kakan(furo_ed_pai,ed_player_id,last_pai,janshi_id,screen,furox,furoy):
			return (furox,furoy)
		furox,furoy,_,_,_,_,_,_=furo_point_and_direction(janshi_id)
		for t in furo_mentsu:
			kind,furo_ed_pai,ed_player_id,last_pai=t
			if kind=='chi' or kind=='pon':
				furox,furoy=draw_chi_or_pon(furo_ed_pai,ed_player_id,last_pai,janshi_id,self.screen,furox,furoy)
			elif kind=='ankan':
				furox,furoy=draw_ankan(furo_ed_pai,ed_player_id,last_pai,janshi_id,self.screen,furox,furoy)
			elif kind=='daiminkan':
				furox,furoy=draw_daiminkan(furo_ed_pai,ed_player_id,last_pai,janshi_id,self.screen,furox,furoy)
			elif kind=='kakan':
				furox,furoy=draw_kakan(furo_ed_pai,ed_player_id,last_pai,janshi_id,self.screen,furox,furoy)
		
		
		
	def draw_kawa(self,sutehai,janshi_id):
		def kawa_rect(id):
			if id==0:
				return (270,480,210,180)
			elif id ==1:
				return (480,270,180,210)
			elif id ==2:
				return (270,90,210,180)
			else: 
				return (90,270,180,210)
		def point_and_direction(janshi_id):
			if janshi_id==0:
				return(270,480,29,0,0,40)
			if janshi_id==1:
				return(480,451,0,-29,40,0)
			if janshi_id==2:
				return(451,230,-29,0,0,-40)
			if janshi_id==3:
				return(230,270,0,29,-40,0)

		self.screen.fill((0,180,0),kawa_rect(janshi_id))
		x,y,vx,vy,vvx,vvy=point_and_direction(janshi_id)
		for i in range(len(sutehai)):
			pai=sutehai[i]
			img=pygame.transform.rotate(pai.image,90*janshi_id)
			self.screen.blit(img,(x+vx*(i%6)+vvx*(i//6),y+vy*(i%6)+vvy*(i//6)))
			if pai in self.taku.dora:
				surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
				surface.fill((255,255,0))
				surface.set_alpha(self.alpha)
				self.screen.blit(surface,(x+vx*(i%6)+vvx*(i//6),y+vy*(i%6)+vvy*(i//6)))
	def draw_oya_mark(self):
		def point_and_direction(i):
			if i==0:
				return (590,610,10,0)
			elif i ==1:
				return (610,100,0,10)
			elif i ==2:
				return (100,100,10,0)
			else: 
				return (100,590,0,10)
		l=['東','南','西','北']
		x,y,dx,dy=point_and_direction(self.taku.ti_tya)
		state=l[(self.taku.kyoku-1)//self.taku.numOfKyoku]
		surface=pygame.transform.rotate(pygame.Surface((60,40)),90*self.taku.ti_tya)
		surface.fill((255,100,71))
		self.screen.blit(surface,(x,y))
		self.screen.blit(pygame.transform.rotate(self.font4.render(state, True, (0,0,0)),90*self.taku.ti_tya), (x+dx,y+dy))
	def draw_naki(self,janshi_id):
		def point(i):
			return 1
		pass
	def draw_center_info(self,taku):
		center_infomation=(270,270,210,210)
		self.screen.fill((100,216,255),center_infomation)
		x,y=270,270
		#残り枚数
		text='残り: '+str(taku.lastOfYama)
		self.screen.blit(self.font2.render(text, True, (0,0,0)), (x+60,y+45))
		#卓情報
		l=['東','南','西','北']
		current_state=l[(taku.kyoku-1)//taku.numOfKyoku]+str((taku.kyoku-1)%taku.numOfKyoku+1)+'局'
		self.screen.blit(self.font3.render(current_state, True, (0,0,0)), (x+60,y+70))
		#積み棒
		tumibo=pygame.transform.smoothscale(pygame.Surface.copy(self.tumibo),(60,6))
		tumi_info=' ×'+str(self.taku.honba)
		self.screen.blit(tumibo, (x+60,y+100+8+5))
		self.screen.blit(self.font1_5.render(tumi_info, True, (0,0,0)), (x+120,y+100+8))
		#供託	
		richibo=pygame.transform.smoothscale(pygame.Surface.copy(self.richibo),(60,6))
		kyotaku_info=' ×'+str(self.taku.kyotaku)
		self.screen.blit(self.font1_5.render(kyotaku_info, True, (0,0,0)), (x+120,y+100+8+15))
		self.screen.blit(richibo, (x+60,y+100+8+15+5))
		#ドラ表示
		vx,vy=x+45-20,y+140
		pre_x=vx
		for i in range(5):
			pai_ura=pygame.Surface((20,30))
			pai_ura.fill(self.back_color_of_pai)
			pre_x=pre_x+20
			self.screen.blit(pai_ura,(pre_x,vy))
			rect=pygame.Rect(pre_x,vy,20,30)
			pygame.draw.rect(self.screen, (0,0,0),rect,2)
		pre_x=vx
		for num in taku.yama.dora_hyouji:
			img=pygame.transform.smoothscale(taku.yama.yama[num].image,(20,30))
			pre_x=pre_x+20
			self.screen.blit(img, (pre_x,vy))
		#点数
		def point_info(i):
			if i==0:
				return (30,170)
			elif i==1:
				return (170,35)
			elif i==2:
				return (35,10)
			else:
				return (10,30)
		def point_richibo(i):
			if i==0:
				return (55,200)
			elif i==1:
				return (200,55)
			elif i==2:
				return (55,0)
			else:
				return (0,55)

		
				
		for i in range(taku.numOfPeople):
			info=l[taku.janshi[i].wind]+': '+str(taku.tokuten.tokuten[i])
			text=self.font3.render(info, True, (0,0,0))
			text=pygame.transform.rotate(text,90*i)
			vx,vy=point_info(i)
			self.screen.blit(text,(x+vx,y+vy))
			#ターンの表示
			if i==self.taku.turn:
				surface=pygame.transform.rotate(pygame.Surface((145,30)),90*i)
				surface.fill((255,0,0))
				surface.set_alpha(self.alpha)
				self.screen.blit(surface,(x+vx,y+vy))
			#リーチ棒の表示
			if taku.janshi[i].richi:
				vx,vy=point_richibo(i)
				richibo=pygame.transform.rotate(self.richibo,90*i)
				self.screen.blit(richibo,(x+vx,y+vy))
	def draw_controller(self):
		#塗り潰し
		self.screen.fill((255,255,0),(750,50,200,700))
		if self.run:
			state= 'run'
			pygame.draw.rect(self.screen, (255, 0, 0), self.button_stop)
			self.screen.blit(self.font4.render('□', True, (0,0,0)), (830,120))
		else:
			state= 'stop'
			pygame.draw.rect(self.screen, (0, 255, 0), self.button_run)
			self.screen.blit(self.font4.render('＞', True, (0,0,0)), (895,120))
			pygame.draw.rect(self.screen, (0, 0, 255), self.button_undo)
			self.screen.blit(self.font4.render('＜', True, (0,0,0)), (765,120))
		if self.taku.state=='finished':
			pygame.draw.rect(self.screen, (0, 0, 255), self.button_new_game)
			self.screen.blit(self.font3.render('new-game', True, (0,0,0)), (780,270))
		self.screen.blit(self.font3.render(state, True, (0,0,0)), (770,70))
			#taku.state
		self.screen.blit(self.font2.render(self.taku.state, True, (0,0,0)), (750,200))
	def button_controll(self,pos):
		if self.run:
			if self.button_stop.collidepoint(pos):
				self.run=False
				return 'stop'
		else:
			if self.button_run.collidepoint(pos):
				self.run=True
				return 'run'
			if self.button_undo.collidepoint(pos):
				return 'undo'
		if self.taku.state=='finished':
			if self.button_new_game.collidepoint(pos):
				return 'new_game'
		return 0
	def draw_kyoku_end(self):
		pass
	def debug(self):
		
		string='environment: '+str(self.taku.environment.state)
		self.screen.blit(self.font1.render(string, True, (0,0,0)), (750,500))
		pass
	def update_display(self):
		self.draw_controller()
		self.draw_oya_mark()
		"""
		if taku.state='kyoku_end':
			self.draw_kyoku_end()
		"""
		self.draw_yama(self.taku.yama)
		self.draw_center_info(self.taku)
		for i in range(self.taku.numOfPeople):
			self.draw_tehai(self.taku.janshi[i].tehai,i,self.taku.janshi[i].furo_mentsu)
			self.draw_kawa(self.taku.janshi[i].sutehai,i)
		"""
		if self.taku.naki_id > -1:
			self.draw_naki(self.taku.naki_id)
		"""
		
		#debug
		self.debug()
	
