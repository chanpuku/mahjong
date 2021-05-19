import pygame
class draw:
	def __init__(self,taku,screen):
			fo='ipamjm.ttf'
			self.font='ipamjm.ttf'
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
			reachbo=pygame.transform.smoothscale(pygame.image.load('image/tennbou-1000.jpg').convert(),(10,100))
			self.reachbo=pygame.transform.rotate(reachbo,90)
			self.back_color_of_pai=(255,190,0)
			self.back_color_of_taku=(0,180,0)
			self.alpha=70
			self.pai_image=self.initialize_pai_image_set()
			self.numOfPeople=self.taku.numOfPeople
	def initialize(self):
		self.draw_chicha_mark()
		self.draw_player_info()
	def initialize_pai_image_set(self):
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
	def get_pai_image(self,pai_id):
		return self.pai_image[pai_id].copy()
	def kyoku_start(self):
		self.screen.fill((0,180,0),(0,0,750,750))# 画面を緑色で塗りつぶす
		self.draw_chicha_mark()
		self.draw_player_info()
	def draw_center_info(self):
		center_infomation=(270,270,210,210)
		#水色
		# self.screen.fill((100,216,255),center_infomation)
		self.screen.fill(pygame.Color('gray'),center_infomation)
		x,y=270,270
		#残り枚数
		text='残り: '+str(self.taku.last_of_yama)
		self.screen.blit(self.font2.render(text, True, (0,0,0)), (x+60,y+45))
		#卓情報
		l=['東','南','西','北']
		current_state=l[(self.taku.kyoku-1)//self.taku.numOfPeople]+str((self.taku.kyoku-1)%self.taku.numOfPeople+1)+'局'
		self.screen.blit(self.font3.render(current_state, True, (0,0,0)), (x+60,y+70))
		#積み棒
		tumibo=pygame.transform.smoothscale(pygame.Surface.copy(self.tumibo),(60,6))
		tumi_info=' ×'+str(self.taku.honba)
		self.screen.blit(tumibo, (x+60,y+100+8+5))
		self.screen.blit(self.font1_5.render(tumi_info, True, (0,0,0)), (x+120,y+100+8))
		#供託	
		reachbo=pygame.transform.smoothscale(pygame.Surface.copy(self.reachbo),(60,6))
		kyotaku_info=' ×'+str(self.taku.kyotaku)
		self.screen.blit(self.font1_5.render(kyotaku_info, True, (0,0,0)), (x+120,y+100+8+15))
		self.screen.blit(reachbo, (x+60,y+100+8+15+5))
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
		for num in self.taku.dora_hyoji_id:
			img=pygame.transform.smoothscale(self.get_pai_image(num),(20,30))
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
		def point_reachbo(i):
			if i==0:
				return (55,200)
			elif i==1:
				return (200,55)
			elif i==2:
				return (55,0)
			else:
				return (0,55)
		for i in range(self.taku.numOfPeople):
			info=l[self.taku.janshi[i].wind]+': '+str(self.taku.janshi[i].mochiten)
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
			if self.taku.janshi[i].reach:
				vx,vy=point_reachbo(i)
				reachbo=pygame.transform.rotate(self.reachbo,90*i)
				self.screen.blit(reachbo,(x+vx,y+vy))
	def draw_tehai(self,janshi_id,tsumo_id=-1,dahai_id=-1):
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
		tehai=self.taku.janshi[janshi_id].tehai
		furo_mentsu=self.taku.janshi[janshi_id].furo_mentsu
		self.screen.fill(self.back_color_of_taku,tehai_rect(janshi_id))
		x,y,vx,vy=point_and_direction(janshi_id)
		tsumo=tsumo_id==janshi_id
		dahai=dahai_id==janshi_id
		for i in range(len(tehai)):
			pai=tehai[i]
			img=self.get_pai_image(pai.correct_id)
			if pai.correct_id in self.taku.dora:
				surface=pygame.Surface((29,40))
				surface.fill(pygame.Color('yellow'))
				surface.set_alpha(self.alpha)
				img.blit(surface,(0,0))
			img=pygame.transform.rotate(img,90*janshi_id)
			if dahai and i==self.taku.janshi[janshi_id].dahai_point:
				x,y=x+vx,y+vy
			vvx,vvy=x+vx*i,y+vy*i
			if  tsumo and  i==len(tehai)-1:
				vvx,vvy=vvx+vx/2,vvy+vy/2
			self.screen.blit(img,(vvx,vvy))
			
			
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
			"""
			print('draw_chi_or_pon')
			print('(furo_ed_pai,ed_player_id,last_pai,janshi_id,screen,furox,furoy)')
			print((furo_ed_pai,ed_player_id,last_pai,janshi_id,screen,furox,furoy))
			print('_,_,dx,dy,rotx,roty,undox,undoy=furo_point_and_direction(janshi_id)')
			print((dx,dy,rotx,roty,undox,undoy))
			"""
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
				if pai.correct_id in self.taku.dora:
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
		
		def draw_nuki(last_pai,janshi_id,screen,furox,furoy):
			def direction(i):
				if i==0:
					return(-29,0)
				if i==1:
					return(0,29)
				if i==2:
					return(29,0)
				if i==3:
					return(0,-29)
			dx,dy=direction(janshi_id)
			x,y=furox,furoy
			pai=last_pai[0]
			img=self.pai_image[pai.correct_id]
			img=pygame.transform.rotate(img,90*janshi_id)
			self.screen.blit(img,(x,y))
			if pai.correct_id in self.taku.dora:
				surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
				surface.fill((255,255,0))
				surface.set_alpha(self.alpha)
				screen.blit(surface,(x,y))
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
			dx,dy=direction(janshi_id)
			x,y=furox,furoy
			for i in range(4):
				if i==1 or i==2:
					pai=last_pai[i]
					img=self.pai_image[pai.correct_id]
					img=pygame.transform.rotate(img,90*janshi_id)
					self.screen.blit(img,(x,y))
					if pai.correct_id in self.taku.dora:
						surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
						surface.fill((255,255,0))
						surface.set_alpha(self.alpha)
						screen.blit(surface,(x,y))
				else:
					surface=pygame.transform.rotate(pygame.Surface((29,40)),90*janshi_id)
					surface.fill(self.back_color_of_pai)
					screen.blit(surface,(x,y))
					w,h=pygame.Surface.get_size(surface)
					pygame.draw.rect(self.screen, pygame.Color('gray'),(x,y,w,h),1)
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
				if pai.correct_id in self.taku.dora:
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
			def can_direction(i):
				if i==0:
					return(0,-29)
				if i==1:
					return(-29,0)
				if i==2:
					return(0,29)
				if i==3:
					return(29,0)
			_,_,dx,dy,rotx,roty,undox,undoy=furo_point_and_direction(janshi_id)
			ddx,ddy=can_direction(janshi_id)
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
					rot_id=(janshi_id+1)%4
					pai=last_pai[2]
					img=self.pai_image[pai.correct_id]
					img=pygame.transform.rotate(img,90*rot_id)
					self.screen.blit(img,(x+ddx,y+ddy))
					if pai.correct_id in self.taku.dora:
						surface=pygame.transform.rotate(pygame.Surface((29,40)),90*rot_id)
						surface.fill((255,255,0))
						surface.set_alpha(self.alpha)
						screen.blit(surface,(x+ddx,y+ddy))
					pai=furo_ed_pai
				else:
					pai=last_pai[k]
					rot_id=janshi_id
					k=k-1
				img=self.pai_image[pai.correct_id]
				img=pygame.transform.rotate(img,90*rot_id)
				self.screen.blit(img,(x,y))
				if pai.correct_id in self.taku.dora:
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
			elif kind=='nuki':
				furox,furoy=draw_nuki(last_pai,janshi_id,self.screen,furox,furoy)
		
	def draw_kawa(self,janshi_id,dahai_id=-1):
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
			#x,y,vx,vy,vvx,vvy,ddx,ddy,rx,ry
			# (point),(1つでのズレ),(1段でのずれ),(打牌時のズレ),(リーチのずれ)
			if janshi_id==0:
				return(270,480,29,0,0,40,8,5,0,0)
			if janshi_id==1:
				return(480,451,0,-29,40,0,5,-8,0,-11)
			if janshi_id==2:
				return(451,230,-29,0,0,-40,-8,-5,-11,11)
			if janshi_id==3:
				return(230,270,0,29,-40,0,-5,8,11,0)

		self.screen.fill((0,180,0),kawa_rect(janshi_id))
		x,y,vx,vy,vvx,vvy,ddx,ddy,rx,ry=point_and_direction(janshi_id)
		vvvx,vvvy=(vx>0)-(vx<0),(vy>0)-(vy<0)#sign関数 >0 =>1,=0 =>0,<0 =>-1
		sutehai=self.taku.janshi[janshi_id].sutehai
		dahai=dahai_id==janshi_id
		reach=False
		for i in range(len(sutehai)):
			pai=sutehai[i]
			pai_img=self.get_pai_image(pai.correct_id)
			#牌情報
			if pai.correct_id in self.taku.dora:
				surface=pygame.Surface((29,40))
				surface.fill(pygame.Color('yellow'))
				surface.set_alpha(self.alpha)
				pai_img.blit(surface,(0,0))
			if  pai.tsumogiri==True:
				surface=pygame.Surface((29,40))
				surface.fill(pygame.Color('black'))
				surface.set_alpha(self.alpha)
				pai_img.blit(surface,(0,0))
			if  not pai.ed_furo_id==-1:
				surface=pygame.Surface((29,40))
				surface.fill(pygame.Color('red'))
				surface.set_alpha(self.alpha)
				pai_img.blit(surface,(0,0))

			if dahai and i==len(sutehai)-1:
				x,y=x+ddx,y+ddy
			if pai.reach_declaration:
				img=pygame.transform.rotate(pai_img,90*(janshi_id+1))
				reach=True
				x,y=x+rx,y+ry
				self.screen.blit(img,(x,y))
				x,y=x-rx-vx+vvvx*40,y-ry-vy+vvvy*40#後に+vx,+vyするので先に引いてる
			else:
				img=pygame.transform.rotate(pai_img,90*janshi_id)
				self.screen.blit(img,(x,y))
			#次のpoint
			x,y=x+vx,y+vy
			if i%6==5:
				x=x-6*vx+vvx
				y=y-6*vy+vvy
				if reach:
					x,y=x-vvvx*40+vx,y-vvvy*40+vy
					reach=False

	def draw_chicha_mark(self):
		def chihca_rect(i):
			if i==0:
				return (590,610,10,0)
			elif i ==1:
				return (610,100,0,10)
			elif i ==2:
				return (100,100,10,0)
			else: 
				return (100,590,0,10)
		l=['東','南','西','北']
		x,y,dx,dy=chihca_rect(self.taku.chicha)
		state=l[(self.taku.kyoku-1)//self.taku.numOfPeople]
		surface=pygame.transform.rotate(pygame.Surface((60,40)),90*self.taku.chicha)
		surface.fill((255,100,71))
		self.screen.blit(surface,(x,y))
		self.screen.blit(pygame.transform.rotate(self.font4.render(state, True, (0,0,0)),90*self.taku.chicha), (x+dx,y+dy))
	def draw_speaking(self,i,type):#発声の表示
		def naki_rect(i):
			if i==0:
				return (140,610,130,50)
			elif i ==1:
				return (610,480,50,130)
			elif i ==2:
				return (480,90,130,50)
			else: 
				return (90,140,50,130)
		x,y,_,_=naki_rect(i)
		if type==-1:#なきなし
			self.screen.fill((0,180,0),naki_rect(i))
		elif type=='REACH':
			self.screen.blit(pygame.transform.rotate(self.font4.render('リーチ', True, (0,0,0)),90*i), (x,y))
		elif type=='chi':
			self.screen.blit(pygame.transform.rotate(self.font5.render('チ ー', True, (0,0,0)),90*i), (x,y))
		elif type=='pon':
			self.screen.blit(pygame.transform.rotate(self.font5.render('ポ ン', True, (0,0,0)),90*i), (x,y))
		elif type=='ron':
			self.screen.blit(pygame.transform.rotate(self.font5.render('ロ ン', True, (0,0,0)),90*i), (x,y))
		elif type=='tsumo':
			self.screen.blit(pygame.transform.rotate(self.font5.render('ツ モ', True, (0,0,0)),90*i), (x,y))
		elif type=='nuki':
			self.screen.blit(pygame.transform.rotate(self.font5.render('ヌ キ', True, (0,0,0)),90*i), (x,y))
		else:#カン
			self.screen.blit(pygame.transform.rotate(self.font5.render('カ ン', True, (0,0,0)),90*i), (x,y))
	def draw_ryukyoku(self):
		font=pygame.font.Font(self.font, 120)
		x,y=250,250
		self.screen.blit(self.font5.render('流 局', True, (0,0,0)), (x,y))
	def draw_player_info(self):
		def info_rect(i):
			if i==0:
				return (490,490,120,110)
			elif i ==1:
				return (490,140,110,120)
			elif i ==2:
				return (140,150,120,110)
			else: 
				return (150,490,110,120)
		def name_point(i):
			if i==0:
				return (495,495,0,0)#(point,修正向き)
			elif i ==1:
				return (495,255,0,-1)
			elif i ==2:
				return (255,255,-1,-1)
			else: 
				return (255,495,-1,0)
		for i in range(self.numOfPeople):
			self.screen.fill((0,200,150),info_rect(i))
			name=self.taku.janshi[i].name
			name_surface=self.font2.render(name, True, (0,0,0))
			w=name_surface.get_width()
			if w>115:
				name_surface=pygame.transform.smoothscale(name_surface,(115,21))
			name_surface=pygame.transform.rotate(name_surface,90*i)
			w,h=name_surface.get_size()
			x,y,dx,dy=name_point(i)
			self.screen.blit(name_surface,(x+dx*w,y+dy*h))
	def draw_kyoku_end(self,data):
		#表示全体
		kyoku_end_display=pygame.Surface((470,470))
		kyoku_end_display.fill((0,0,0))
		kyoku_end_display.set_alpha(235)
		
		
		#翻符点数
		#役
		#供託、本場
		#ドラ
		#持ち点,移動
		


		point=(140,140)
		self.screen.blit(kyoku_end_display,point)
	def draw_game_end(self):
		pass
	def draw_taku(self,tsumo_id=-1,dahai_id=-1):
		self.draw_center_info()
		for i in range(self.numOfPeople):
			self.draw_kawa(i,dahai_id=dahai_id)
			self.draw_tehai(i,tsumo_id=tsumo_id,dahai_id=dahai_id)
			self.draw_speaking(i,-1)
	