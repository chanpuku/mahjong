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
			self.font5=pygame.font.Font(fo, 50)
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
			self.pai_image=self.get_pai_image()
	def get_pai_image(self):
		l=[]
		for i in range(37):
			if i<9:name='m'+str(i+1)
			elif i<18:name='p'+str(i-8)
			elif i<27:name='s'+str(i-17)
			elif i<34:name='z'+str(i-26)
			elif i==34:name='m5+'
			elif i==35:name='p5+'
			elif i==36:name='s5+'
			l.append(pygame.image.load('image/'+name+'.jpg').convert() )
		return l
	def screen_initialize(self):
		self.screen.fill((0,180,0),(0,0,750,750))# 画面を緑色で塗りつぶす
		self.screen.fill((255,255,0),(750,0,200,750))# 山との間を塗りつぶす
		self.screen.fill((0,180,0),(950,0,450,750))# 山部分を塗りつぶす
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
		kan_times=self.taku.kan_times
		for i in range(length+kan_times):
			if i<kan_times:
				continue
			img=self.pai_image[yama.yama[i-kan_times].correct_id]
			img=pygame.transform.rotate(img,-90)
			self.screen.blit(img, point(i))
		#終了場所
		last_pai=length-self.taku.lastOfYama
		x,y=point(last_pai)
		self.screen.fill((255,0,190),(x,y+29,40,10))
		#表示牌
		for i in yama.dora_hyoji:
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
			img=self.pai_image[pai.correct_id]
			img=pygame.transform.rotate(img,90*janshi_id)
			vvx,vvy=x+vx*i,y+vy*i
			if  janshi_id==self.taku.turn and  i==len(tehai)-1 and self.taku.state=='tsumo_action' and not self.taku.furo_type=='pon' and not self.taku.furo_type=='chi':
				vvx,vvy=vvx+vx/2,vvy+vy/2
			self.screen.blit(img,(vvx,vvy))
			if pai in self.taku.dora:
				surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
				surface.fill((255,255,0))
				surface.set_alpha(self.alpha)
				self.screen.blit(surface,(vvx,vvy))
			
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
				img=self.pai_image[pai.correct_id]
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
		
		def draw_ankan(last_pai,janshi_id,screen,furox,furoy):
			def direction(i):
				if i==0:
					return(-29,0)
				if i==1:
					return(0,29)
				if i==2:
					return(29,0)
				if i==3:
					return(0,-29)
			dx,dy,=direction(janshi_id)
			x,y=furox,furoy
			for i in range(4):
				if i==1 or i==2:
					pai=last_pai[i]
					img=self.pai_image[pai.correct_id]
					img=pygame.transform.rotate(img,90*janshi_id)
					self.screen.blit(img,(x,y))
					if pai in self.taku.dora:
						surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
						surface.fill((255,255,0))
						surface.set_alpha(self.alpha)
						screen.blit(surface,(x,y))
				else:
					surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
					surface.fill((self.back_color_of_pai,0))
					screen.blit(surface,(x,y))
				x+=dx
				y+=dy
			return(x,y)
		
			
		def draw_daiminkan(furo_ed_pai,ed_player_id,last_pai,janshi_id,screen,furox,furoy):
			_,_,dx,dy,rotx,roty,undox,undoy=furo_point_and_direction(janshi_id)
			x,y=furox,furoy
			if ed_player_id<janshi_id:
				d=ed_player_id-janshi_id+3
			else:d=ed_player_id-janshi_id-1
			if d==2:d=3
			k=1
			for i in range(4):
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
				img=self.pai_image[pai.correct_id]
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
		def draw_kakan(furo_ed_pai,ed_player_id,last_pai,janshi_id,screen,furox,furoy):
			return (furox,furoy)
		furox,furoy,_,_,_,_,_,_=furo_point_and_direction(janshi_id)
		for t in furo_mentsu:
			kind,furo_ed_pai,ed_player_id,last_pai=t
			if kind=='chi' or kind=='pon':
				furox,furoy=draw_chi_or_pon(furo_ed_pai,ed_player_id,last_pai,janshi_id,self.screen,furox,furoy)
			elif kind=='ankan':
				#全てlast_pai
				furox,furoy=draw_ankan(last_pai,janshi_id,self.screen,furox,furoy)
			elif kind=='daiminkan':
				furox,furoy=draw_daiminkan(furo_ed_pai,ed_player_id,last_pai,janshi_id,self.screen,furox,furoy)
			elif kind=='kakan':
				#last_paiの最後が加えたpai
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
			img=pygame.transform.rotate(self.pai_image[pai.correct_id],90*janshi_id)
			self.screen.blit(img,(x+vx*(i%6)+vvx*(i//6),y+vy*(i%6)+vvy*(i//6)))
			if pai in self.taku.dora:
				surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
				surface.fill((255,255,0))
				surface.set_alpha(self.alpha)
				self.screen.blit(surface,(x+vx*(i%6)+vvx*(i//6),y+vy*(i%6)+vvy*(i//6)))
			if not pai.ed_furo_id==-1:
				surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
				surface.fill(pygame.Color('black'))
				surface.set_alpha(self.alpha)
				self.screen.blit(surface,(x+vx*(i%6)+vvx*(i//6),y+vy*(i%6)+vvy*(i//6)))
	def draw_chicha_mark(self):
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
		x,y,dx,dy=point_and_direction(self.taku.chicha)
		state=l[(self.taku.kyoku-1)//self.taku.numOfKyoku]
		surface=pygame.transform.rotate(pygame.Surface((60,40)),90*self.taku.chicha)
		surface.fill((255,100,71))
		self.screen.blit(surface,(x,y))
		self.screen.blit(pygame.transform.rotate(self.font4.render(state, True, (0,0,0)),90*self.taku.chicha), (x+dx,y+dy))
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
		for num in taku.yama.dora_hyoji:
			img=pygame.transform.smoothscale(self.pai_image[taku.yama.yama[num].correct_id],(20,30))
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
		self.screen.fill((255,255,0),(750,50,200,400))#上400,下350はdebug
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
		return 'run'
	def draw_kyoku_end(self):#自由に書き換えて良い
		
		def point(i):
			if i==0:
				return (90,200)
			elif i==1:
				return (200,55)
			elif i==2:
				return (55,-5)
			else:
				return (-5,90)
		x,y=270,270
		cur_tokuten=self.taku.paifu['kyoku'][-1]['end']['score']
		pre_tokuten=self.taku.paifu['kyoku'][-1]['info']['score']
		for i in range(self.taku.numOfPeople):
			
			d=cur_tokuten[i]-pre_tokuten[i]
			if not d==0:
				if d>0:
					text=self.font2.render(str('+')+str(d), True, pygame.Color('blue'))
				else:
					text=self.font2.render(str(d), True, pygame.Color('red'))
				vx,vy=point(i)
				text=pygame.transform.rotate(text,90*i)
				self.screen.blit(text, (x+vx,y+vy))
		#self.draw_furo()

	def draw_furo(self):
		def point(i):
			if i==0:
				return (315,640)
			elif i==1:
				return (640,315)
			elif i==2:
				return (315,60)
			else:
				return (60,315)
		if self.taku.furo_happen:
			typ=self.taku.furo_type
			if not typ=='ron':
				if typ=='pon':s='ポ ン'
				elif typ=='chi':s='チ ー'
				elif typ=='tsumo':s='ツ モ'
				else:s='カ ン'
				x,y=point(self.taku.furo_id)
				text=self.font5.render(s, True, (0,0,0))
				text=pygame.transform.rotate(text,90*self.taku.furo_id)
				self.screen.blit(text, (x,y))
			else:
				s='ロ ン'
				for t in self.taku.hora_list:
					x,y=point(t[0])
					text=self.font5.render(s, True, (0,0,0))
					text=pygame.transform.rotate(text,90*t[0])
					self.screen.blit(text, (x,y))
	def debug(self,x=None):
		self.screen.fill(pygame.Color('black'),(750,450,200,300))#下300,上400はcontroller
		l=[]
		s1='environment'
		s2=str(self.taku.environment.state[18:27])
		s3=str(self.taku.environment.state[27:34])
		
		l.append(s1)
		l.append(s2)
		l.append(s3)
		for i in range(len(l)):
			self.screen.blit(self.font1.render(l[i], True, pygame.Color('white')), (750,500+20*i))
		
	def update_display(self):
		self.draw_controller()
		self.draw_chicha_mark()
		self.draw_center_info(self.taku)
		
		#'takuのkyoku_end'の直後
		#if self.taku.state=='kyoku_start':self.draw_kyoku_end()

		self.draw_yama(self.taku.yama)
		for i in range(self.taku.numOfPeople):
			self.draw_tehai(self.taku.janshi[i].tehai,i,self.taku.janshi[i].furo_mentsu)
			self.draw_kawa(self.taku.janshi[i].sutehai,i)#はみ出すかもなのでdraw_tehaiとの順番大事
		
		self.draw_furo()
		
		#debug
		self.debug()
	
