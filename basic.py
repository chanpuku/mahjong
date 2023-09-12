# -*- coding: utf-8 -*-
import random
import pygame
import tehai_func
import numpy as np

KIND_OF_PAI=34
KIND_OF_PAI_NOMAL=37

class pai:
	def __init__(self,typ,num,dora=False,aka=False,id=None):
		if not id==None:
			if id<9:
				typ='m'
				num=id+1
			elif id<18:
				typ='p'
				num=id%9+1
			elif id<27:
				typ='s'
				num=id%9+1
			elif id<34:
				typ='z'
				num=id%9+1
			elif id<37:
				if id==34:typ='m'
				elif id==35:typ='p'
				elif id==36:typ='s'
				num=5
				dora=True
				aka=True
		self.typ=typ
		self.num=num
		self.name=str(typ)+str(num)
		if typ=='m':tp=0
		elif typ=='p':tp=9
		elif typ=='s':tp=18
		else:tp=27
		self.id=num+tp-1
		self.correct_id=self.id
		self.aka=aka
		if aka:
			self.name=self.name+'+'
			if typ=='m':self.correct_id=34
			elif typ=='p':self.correct_id=35
			elif typ=='s':self.correct_id=36
		self.tsumogiri=False
		self.reach_declaration=False
		self.ed_furo_id=-1
		self.ed_furo_type=None	
		self.dora=dora
		#self.image=pygame.image.load('image/'+self.name+'.jpg').convert() 
		
	def next(self):
		if self.typ=='z':
			if self.num<=4:
				num=self.num%4+1
			else:
				num=(self.num-4)%3+5
		else:
			num=self.num%9+1
		return pai(self.typ,num)
	def __lt__(self,other):
		#self < other 
		if self.typ==other.typ:
			return self.num<other.num
		else:
			return self.typ<other.typ 
	def __str__(self):
		return self.name
	def __eq__(self,other):
		return  self.typ==other.typ and self.num==other.num and self.aka==other.aka

	
class yama:
	#一局ごとにあたらしいのが作られてる
	def __init__(self,numOfPeople,numOfAkadora,pointOfDoraHyoji,jihai=True):
		self.numOfPeople=numOfPeople
		self.numOfAkadora=numOfAkadora
		self.jihai=jihai
		self.pointOfDoraHyoji=pointOfDoraHyoji
		self.kan_times=0
		typ_list=['m','p','s','z']
		self.yama=[]
		if self.numOfPeople==4:
			for typ in typ_list:
				for num in range(1,10):
					for i in range(4):
						if num==5 and (not typ=='z') and i<self.numOfAkadora:
							self.yama.append(pai(typ,num,dora=True,aka=True))
							#self.dora.append(pai(typ,num,aka=True))
						else :self.yama.append(pai(typ,num))
					if num==7 and typ=='z':
						break
		elif self.numOfPeople==3:
			for typ in typ_list:
				for num in range(1,10):
					if num>1 and num<9 and typ=='m':
						continue
					for i in range(4):
						if num==5 and (not typ=='z') and i<numOfAkadora:
							self.yama.append(pai(typ,num,dora=True,aka=True))
						else :self.yama.append(pai(typ,num))
					if num==7 and typ=='z':
						break
		elif self.numOfPeople==2:
			typ_list=['s']
			if self.jihai:
				typ_list.append('z')
			for typ in typ_list:
				for num in range(1,10):
					for i in range(4):
						if num==5 and (not typ=='z') and i<self.numOfAkadora:
							self.yama.append(pai(typ,num,dora=True,aka=True))
						else :self.yama.append(pai(typ,num))
					if num==7 and typ=='z':
						break
		random.shuffle(self.yama)
		self.dora_hyoji=[self.yama[i].correct_id for i in self.pointOfDoraHyoji]
		self.dora=[self.yama[i].next().correct_id for i in self.pointOfDoraHyoji]
		if self.numOfAkadora:
			self.dora+=[34,35,36]

	def pop(self):
		return self.yama.pop()
	def __len__(self):
		return len(self.yama)
	def kan(self):
		self.kan_times+=1
		self.pointOfDoraHyoji.append(self.pointOfDoraHyoji[-1]+2)
		self.dora_hyoji.append(self.yama[self.pointOfDoraHyoji[-1]].correct_id)
		self.dora.append(self.yama[self.pointOfDoraHyoji[-1]].next().correct_id)
		pai=self.yama.pop(0)
		for i in range(len(self.pointOfDoraHyoji)):
			self.pointOfDoraHyoji[i]-=1
		return pai
	def make(self,forward_id_list,tsumo_id_list=[],back_id_list=[]):
		f=[]
		t=[]
		b=[]
		for i in forward_id_list[::-1]:
			for j in range(len(self.yama)):
				if self.yama[j].id==i:
					f.append(self.yama.pop(j))
					break
		for i in tsumo_id_list[::-1]:
			for j in range(len(self.yama)):
				if self.yama[j].id==i:
					t.append(self.yama.pop(j))
					break
		for i in back_id_list[::-1]:
			for j in range(len(self.yama)):
				if self.yama[j].id==i:
					b.append(self.yama.pop(j))
					break
		j=max(0,self.numOfPeople*13-len(f))
		self.yama=b+self.yama[j:]+t+self.yama[:j]+f
		self.dora_hyoji=[self.yama[i].correct_id for i in self.pointOfDoraHyoji]
		self.dora=[self.yama[i].next().correct_id for i in self.pointOfDoraHyoji]
		if self.numOfAkadora:
			self.dora+=[34,35,36]

class janshi:
	def __init__(self,mochiten,name=None):
		self.mochiten=mochiten
		self.tehai=[]
		self.furo_mentsu=[]#type,furo_ed_pai,ed_player_id,reveal_pai_list
		self.tehai_state=[]
		self.sutehai=[]
		self.tenpai=False
		self.reach=False
		self.furiten=False
		self.can_furo_dic={'pon':set(),'chi':0,'daiminkan':0,'ron':0}
		self.wind=0
		self.menzen=True
		self.player_id=None
		self.name=name
	def game_start(self,id):
		self.plyaer_id=id
	def kyoku_start(self,wind):
		self.tehai=[]
		self.furo_mentsu=[]
		self.dora_hyoji=[]
		self.sutehai=[]
		self.tenpai=False
		self.reach=False
		self.furiten=False
		self.can_furo_dic={'pon':set(),'chi':0,'daiminkan':0,'ron':0}
		self.wind=wind
		self.menzen=True
	def is_tempai(self):
		l=tehai_func.vectorize_pai_list(self.tehai)
		if tehai_func.Shanten(l)==0:
			return True
		else:
			return False
		

class nomal_agent(janshi):
	"""
	def __init__(self,mochiten):
		self.mochiten=mochiten
		self.tehai=[]
		self.furo_mentsu=[]#type,furo_ed_pai,ed_player_id,reveal_pai_list
		self.tehai_state=[]
		self.sutehai=[]
		self.tenpai=False
		self.reach=False
		self.furiten=False
		self.can_furo_dic={'pon':set(),'chi':0,'daiminkan':0,'ron':0}
		self.wind=0
		self.menzen=True
		self.player_id=None
	"""
	def game_start(self,id):
		self.plyaer_id=id
	def kyoku_start(self,wind):
		self.tehai=[]
		self.furo_mentsu=[]
		self.dora_hyoji=[]
		self.sutehai=[]
		self.tenpai=False
		self.reach=False
		self.furiten=False
		self.can_furo_dic={'pon':set(),'chi':0,'daiminkan':0,'ron':0}
		self.wind=wind
		self.menzen=True
	def getting_haipai(self):
		#haipai,dora_hyojiはtakuに教えられる
		#その時に呼ばれる関数
		"""###テスト
		l=[]
		for i in range(3):
			l.append(self.tehai.pop())
		self.furo_mentsu.append(('chi',l[1],3,[l[0],l[2]]))
		l=[]
		for i in range(3):
			l.append(self.tehai.pop())
		self.furo_mentsu.append(('pon',l[1],3,[l[0],l[2]]))
		"""
		self.tehai_state=np.zeros(KIND_OF_PAI_NOMAL)
		for p in self.tehai:
			self.tehai_state[p.correct_id]+=1
		self.make_can_furo_dic()
		
	def tsumo(self,yama,pai=None):
		if not pai:pai=yama.pop()
		#なんらかの判定
		self.tehai.append(pai)
		self.tehai_state[pai.correct_id]+=1

		return pai
	def action(self,environment,tsumo_pai=0,furo=False):
		if  furo:
			rd=self.dahai_choice(self.tehai_state,environment,len(self.furo_mentsu),tsumo_pai=tsumo_pai)
			k=0
			pai=0
			for i in range(len(self.tehai)):
				if self.tehai[i].correct_id==rd:
					k=i
					break
			pai=self.tehai[k]
			self.sutehai.append(pai)
			self.tehai_state[rd]-=1
			del self.tehai[k]
			self.tehai.sort()
			self.make_can_furo_dic()
			return ('dahai',pai)
		else:
			state=tehai_func.correct_id_state_to_id_state(self.tehai_state)
			tsumo,rt=self.tsumo_check(tsumo_pai,environment)
			ankan,ra=self.ankan_check(state,tsumo_pai,environment)
			kakan,rk=self.kakan_check(state,tsumo_pai,environment)
			#タクティクス
			if tsumo:
				return('tsumo',rt)
			elif kakan:
				pai=self.kakan(rk)
				return('kakan',pai)
			elif ankan:
				self.ankan(ra)
				return('ankan',0)
			else:
				rd=self.dahai_choice(self.tehai_state,environment,len(self.furo_mentsu),tsumo_pai=tsumo_pai)
				k=0
				pai=0
				for i in range(len(self.tehai)):
					if self.tehai[i].correct_id==rd:
						k=i
						break
				pai=self.tehai[k]
				self.sutehai.append(pai)
				self.tehai_state[rd]-=1
				del self.tehai[k]
				self.tehai.sort()
				self.make_can_furo_dic()
				return ('dahai',pai)
	def dahai_choice(self,state,environment,num_of_furoMentsu,tsumo_pai=0):
		#打牌ロジック
		s,si,uke=10,-1,0
		state=tehai_func.correct_id_state_to_id_state(self.tehai_state)
		for i in range(len(state)):
			if state[i]==0:continue
			state[i]-=1
			a=tehai_func.Shanten(state,num_of_furoMentsu=num_of_furoMentsu)
			u=0
			for k in tehai_func.ukeire(state,num_of_furoMentsu=num_of_furoMentsu):
				u+=(4-state[k]-environment.state[k])
			if a<s:
				s,si,uke=a,i,u
			elif a==s :
				if u>uke:
					s,si,uke=a,i,u
				elif u==uke:
					if si in environment.dora:
						s,si,uke=a,i,u
			state[i]+=1
		return si
	def kakan_check(self,state,tsumo_pai,environment):
		if environment.kan_times==4 or environment.last_of_yama<2:
			return False,-1
		cur_s=tehai_func.Shanten(self.tehai_state,num_of_furoMentsu=len(self.furo_mentsu))
		cur_u=0
		for k in tehai_func.ukeire(self.tehai_state,num_of_furoMentsu=len(self.furo_mentsu)):
			cur_u+=(4-state[k]-environment.state[k])
		l=[]
		for f in self.furo_mentsu:
			if f[0]=='pon' and state[f[1].id]:
				l.append(f[1].id)
		id=-1
		for i in l:
			state[i]-=1
			s=tehai_func.Shanten(state,num_of_furoMentsu=len(self.furo_mentsu))
			u=0
			for k in tehai_func.ukeire(self.tehai_state,num_of_furoMentsu=len(self.furo_mentsu)):
				u+=(4-state[k]-environment.state[k])
			if cur_s>=s and cur_u<=u:
				cur_s,cur_u,id=s,u,i
		if id<0:
			return False,-1
		else:
			return True,id
	def ankan_check(self,state,tsumo_pai,environment):
		if environment.kan_times==4 or environment.last_of_yama<2:
			return False,-1
		cur_s=tehai_func.Shanten(self.tehai_state,num_of_furoMentsu=len(self.furo_mentsu))
		cur_u=0
		for k in tehai_func.ukeire(self.tehai_state,num_of_furoMentsu=len(self.furo_mentsu)):
			cur_u+=(4-state[k]-environment.state[k])
		l=[]
		for i in range(len(state)):
			if state[i]==4:l.append(i)
		id=-1
		for i in l:
			state[i]-=1
			s=tehai_func.Shanten(state,num_of_furoMentsu=len(self.furo_mentsu))
			u=0
			for k in tehai_func.ukeire(self.tehai_state,num_of_furoMentsu=len(self.furo_mentsu)):
				u+=(4-state[k]-environment.state[k])
			if cur_s>=s and cur_u<=u:
				cur_s,cur_u,id=s,u,i
		if id<0:
			return False,-1
		else:
			return True,id
	def tsumo_check(self,tsumo_pai,environment):
		han=4
		fu=30
		if tsumo_pai.id in self.can_furo_dic['ron']:
			return True,(han,fu)
		else:return False,(han,fu)
	def ron_check(self,dahai):
		if self.furiten_check(dahai.id):
			return False
		elif dahai.id in self.can_furo_dic['ron']:
			return True
		else:
			return False
	def chi_check(self,dahai,cur_s,cur_u,environment,state):
		#(するか,typ,シャンテン数,受け入れ,さらし)
		if not dahai.id in self.can_furo_dic['chi']:
			return False,'chi',10,0,[]
		else:
			t=None
			for id1,id2 in tehai_func.can_chi_list(self.tehai_state,dahai.id):
				self.tehai_state[id1]-=1
				self.tehai_state[id2]-=1
				pai_id=self.dahai_choice(self.tehai_state,environment,len(self.furo_mentsu)+1)
				self.tehai_state[pai_id]-=1
				s=tehai_func.Shanten(self.tehai_state,len(self.furo_mentsu)+1)
				u_l=tehai_func.ukeire(self.tehai_state,len(self.furo_mentsu)+1)
				u=0
				self.tehai_state[pai_id]+=1
				self.tehai_state[id1]+=1
				self.tehai_state[id2]+=1
				for i in u_l:
					u+=(4-self.tehai_state[i]-environment.state[i])
				if cur_s>s :
					cur_s,cur_u,t=s,u,(id1,id2)
				elif cur_s==s:
					if cur_u<u:
						cur_s,cur_u,t=s,u,(id1,id2)
					elif cur_u==u:
						if id1>33 or id2>33:
							cur_s,cur_u,t=s,u,(id1,id2)
				
			if t:
				#さらしリストを作る
				l=[]
				j=0
				for i in range(len(self.tehai)):
					if self.tehai[i].correct_id==t[j]:
						l.append(i)
						if j==0:
							j+=1
							continue
						else:break
				return  True,'chi',s,u,l
			else:
				return False,'chi',10,0,[]
	def pon_check(self,dahai,cur_s,cur_u,environment,state):
		if not dahai.id in self.can_furo_dic['pon']:
			return False,'pon',10,0,[]
		l=[]
		j=0
		#さらしリストを作る
		for i in range(len(self.tehai)):
			if self.tehai[-(i+1)].id==dahai.id:
				l.append(len(self.tehai)-(i+1))
				j+=1
				if j>1:break
		l.sort()
		state[dahai.id]-=2
		pai_id=self.dahai_choice(state,environment,len(self.furo_mentsu)+1)
		state[pai_id]-=1
		s=tehai_func.Shanten(state,len(self.furo_mentsu)+1)
		u_l=tehai_func.ukeire(state,len(self.furo_mentsu)+1)
		u=0
		state[pai_id]+=1
		state[dahai.id]+=2
		for i in u_l:
			u+=(4-self.tehai_state[i]-environment.state[i])
		if cur_s>s or (cur_s==s and cur_u<u ):
			return(True,'pon',s,u,l)
		else:return (False,'pon',10,0,[])
	def daiminikan_check(self,dahai,cur_s,cur_u,environment,state):
		if environment.kan_times==4 or environment.last_of_yama<2:
			return (False,'daiminkan',10,0,[])
		if not dahai.id in self.can_furo_dic['daiminkan']:
			return False,'diminkan',10,0,[]
		#debug
		
		l=[]
		j=0
		for i in range(len(self.tehai)):
			if self.tehai[i].id==dahai.id:
				l.append(i)
				j+=1
				if j>3:break
		state[dahai.id]-=3
		s=tehai_func.Shanten(state,len(self.furo_mentsu)+1)
		u_l=tehai_func.ukeire(state,len(self.furo_mentsu)+1)
		state[dahai.id]+=3
		u=0
		for i in u_l:
			u+=(4-environment.state[i]-state[i])
		if cur_s>=s and cur_u<=u :return(True,'daiminkan',s,u,l)
		else:return (False,'daiminkan',10,0,[])

	def furo_check(self,dahai,can_chi,environment,chankan=False):
		#(bool,typ,pai,さらしリスト)

		state=tehai_func.correct_id_state_to_id_state(self.tehai_state)

		if self.ron_check(dahai):
			return (True,'ron',0)
		elif chankan:
			return(False,0,0)
		else:
			cur_s=tehai_func.Shanten(self.tehai_state,len(self.furo_mentsu))
			cur_u_l=tehai_func.ukeire(self.tehai_state,len(self.furo_mentsu))
			cur_u=0
			for i in cur_u_l:
				cur_u+=(4-environment.state[i]-state[i])
			if can_chi:f_l=[self.daiminikan_check,self.pon_check,self.chi_check]
			else:f_l=[self.daiminikan_check,self.pon_check]
			boo,typ,shan,uke,li=False,0,10,0,[]
			#Trueの中で最もいいやつを使う
			for f in f_l:
				b,t,s,u,l=f(dahai,cur_s,cur_u,environment,state)
				if b :
					if shan>s or (shan==s and uke<u):
						boo,typ,shan,uke,li=b,t,s,u,l
			return (boo,typ,li)
	def furiten_check(self,pai_id):
		return pai_id in [pai.id for pai in self.sutehai]
	def make_can_furo_dic(self):
		self.can_furo_dic=tehai_func.can_furo_dic(self.tehai_state,len(self.furo_mentsu))
		furi=set()
		for p in self.sutehai:
			furi.add(p.id)
		for i in self.can_furo_dic['ron']:
			if i in furi:
				self.furiten=True
				break
		else:
			self.furiten=False
	
	def furo(self,typ,pai,ed_player_id,l):
		#'kakan','ankan'はここに来ない
		l.sort()
		self.furo_mentsu.append([typ,pai,ed_player_id,[self.tehai[i] for i in l]])
		j=0
		for i in l:
			self.tehai_state[self.tehai[i-j].correct_id]-=1
			del self.tehai[i-j]
			j+=1
	def kakan(self,id):
		point=0
		for i in range(len(self.tehai)):
			if self.tehai[i].id==id:
				point=i
				break
		pai=self.tehai[point]
		del self.tehai[point]
		self.tehai_state[pai.correct_id]-=1
		for i in range(len(self.furo_mentsu)):
			if self.furo_mentsu[i][1].id==pai.id:
				self.furo_mentsu[i][0]='kakan'
				self.furo_mentsu[i][3].append(pai)
				break
		return pai
	def ankan(self,id):
		l=[]
		j=0
		for i in range(len(self.tehai)):
			if self.tehai[i-j].id==id:
				l.append(self.tehai[i-j])
				self.tehai_state[self.tehai[i-j].correct_id]-=1
				pai=self.tehai.pop(i-j)
				j+=1
		self.furo_mentsu.append(['ankan',pai,-1,l])
	
	def nuki(self,id):
		l=[]
		for i in range(len(self.tehai)):
			if self.tehai[i].id==id:
				l.append(self.tehai[i])
				self.tehai_state[self.tehai[i].correct_id]-=1
				pai=self.tehai.pop(i)
				break
		self.furo_mentsu.append(['nuki',pai,-1,l])
	