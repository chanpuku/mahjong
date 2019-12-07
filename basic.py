# -*- coding: utf-8 -*-
import random
import pygame
import tehai_func
import numpy as np

KIND_OF_PAI=34
KIND_OF_PAI_NOMAL=37

class pai:
	def __init__(self,typ,num,dora=False,aka=False):
		self.typ=typ
		self.num=num
		self.name=typ+str(num)
		if typ=='m':tp=0
		elif typ=='p':tp=9
		elif typ=='s':tp=18
		else:tp=27
		self.id=num+tp-1
		self.correct_id=self.id
		self.aka=aka
		if aka:
			if typ=='m':self.correct_id=34
			elif typ=='p':self.correct_id=35
			elif typ=='s':self.correct_id=36
		self.tsumogiri=False
		self.ed_furo_id=-1
		self.ed_furo_type=None
		if dora:
			self.name=self.name+'+'
		self.dora=dora
		self.image=pygame.image.load('image/'+self.name+'.jpg').convert() 
		
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
	def __init__(self,numOfPeople,numOfAkadora,pointOfDora,jihai=True):
		self.numOfPeople=numOfPeople
		self.numOfAkadora=numOfAkadora
		self.jihai=jihai
		self.pointOfDora=pointOfDora
		typ_list=['m','p','s','z']
		self.yama=[]
		self.dora_hyouji=[self.pointOfDora]
		self.dora=[]
		if self.numOfPeople==4:
			for typ in typ_list:
				for num in range(1,10):
					for i in range(4):
						if num==5 and (not typ=='z') and i<self.numOfAkadora:
							self.yama.append(pai(typ,num,dora=True,aka=True))
							self.dora.append(pai(typ,num,aka=True))
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
							self.dora.append(pai(typ,num,aka=True))
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
							self.yama.append(pai(typ,num,dora=True))
							self.dora.append(pai(typ,num))
						else :self.yama.append(pai(typ,num))
					if num==7 and typ=='z':
						break
		random.shuffle(self.yama)
		for num in self.dora_hyouji:
			self.dora.append(self.yama[num].next())

	def pop(self):
		return self.yama.pop()
	def __len__(self):
		return len(self.yama)
class janshi:
	def __init__(self,mochiten):
		self.mochiten=mochiten
		self.tehai=[]
		self.furo_mentsu=[]#kind,furo_ed_pai,ed_player_id,last_pai
		self.tehai_state=[]
		self.environment_state_correct=[]
		self.environment_state=[]
		self.sutehai=[]
		self.tenpai=False
		self.richi=False
		self.furiten=False
		self.can_furo_dic={'pon':set(),'chi':0,'daiminkan':0,'ron':0}
		self.wind=0
		self.menzen=True
		self.player_id=None
	def game_start(self,id):
		self.plyaer_id=id
	def kyoku_start(self,wind):
		self.environment_state_correct=[]
		self.environment_state=[]
		self.tehai=[]
		self.furo_mentsu=[]
		self.tehai_state=[]
		self.dora_hyoji=[]
		self.sutehai=[]
		self.tenpai=False
		self.richi=False
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
		self.environment_state=np.zeros(KIND_OF_PAI)
		self.environment_state_correct=np.zeros(KIND_OF_PAI_NOMAL)
		self.tehai_state=np.zeros(KIND_OF_PAI)
		for p in self.tehai:
			self.environment_state_correct[p.correct_id]+=1
			self.environment_state[p.id]+=1
			self.tehai_state[p.id]+=1
		self.environment_state_correct[self.dora_hyoji[0].correct_id]+=1
		self.environment_state[self.dora_hyoji[0].id]+=1
		self.make_can_furo_dic(self.tehai_state,len(self.furo_mentsu))
		
	def tsumo(self,yama,kan=False):
		pai=yama.pop()
		#なんらかの判定
		self.tehai.append(pai)
		self.tehai_state[pai.id]+=1
		self.environment_state_correct[pai.correct_id]+=1
		self.environment_state[pai.id]+=1
		return pai
	def action(self,hora=False,tsumo_pai=0):
		if  hora:
			rd=self.dahai_choice()
			pai=self.tehai[rd]
			self.sutehai.append(pai)
			self.tehai_state[pai.id]-=1
			del self.tehai[rd]
			self.tehai.sort()
			self.make_can_furo_dic(self.tehai_state,len(self.furo_mentsu))
			return ('dahai',pai)
		else:
			tsumo,rt=self.tsumo_check(tsumo_pai)
			ankan,ra=self.ankan_check(tsumo_pai)
			kakan,rk=self.kakan_check(tsumo_pai)
			#タクティクス
			if tsumo:
				return('tsumo',rt)
			elif kakan:
				return('kakan',rk)
			elif ankan:
				return('ankan',ra)
			else:
				rd=self.dahai_choice(tsumo_pai=tsumo_pai)
				pai=self.tehai[rd]
				self.sutehai.append(pai)
				self.tehai_state[pai.id]-=1
				del self.tehai[rd]
				self.tehai.sort()
				self.make_can_furo_dic(self.tehai_state,len(self.furo_mentsu))
				return ('dahai',pai)
	def dahai_choice(self,tsumo_pai=0):
		#打牌ロジック
		s,si,uke=10,-1,0
		for i in range(len(self.tehai)):
			j=self.tehai[i].id
			self.tehai_state[j]-=1
			a=tehai_func.Shanten(self.tehai_state,num_of_furoMentsu=len(self.furo_mentsu))
			u=0
			for k in tehai_func.ukeire(self.tehai_state):
				u+=(4-self.tehai_state[k])
			if a<s:
				s,si,uke=a,i,u
			elif a==s :
				if u>uke:
					s,si,uke=a,i,u
				elif u==uke:
					if self.tehai[si].dora:
						s,si,uke=a,i,u
			self.tehai_state[j]+=1
		return si
	def kakan_check(self,tusmo_pai):
		return False,-1
	def ankan_check(self,tusmo_pai):
		return False,-1
	def tsumo_check(self,tusmo_pai):
		han=4
		fu=30
		if tusmo_pai.id in self.can_furo_dic['ron']:
			return True,(han,fu)
		else:return False,(han,fu)

	def furo_check(self,dahai,):
		#(bool,typ,pai,さらしリスト)
		def ron_check(dahai):
			if dahai.id in self.can_furo_dic['ron']:
				return True
			else:
				return False	
		def chi_check(dahai,cur_s,cur_u):
			
			return False,'daiminkan',10,0,[]
			#(するか,typ,シャンテン数,受け入れ,さらし)
			if not dahai.id in self.can_furo_dic['chi']:
				return False,'chi',10,0,[]
			
		def pon_check(dahai,cur_s,cur_u):
			if not dahai.id in self.can_furo_dic['pon']:
				return False,'pon',10,0,[]
			l=[]
			j=0
			for i in range(len(self.tehai)):
				if self.tehai[i].id==dahai.id:
					l.append(i)
					j+=1
					if j>2:break
			self.tehai_state[dahai.id]-=2
			s=tehai_func.Shanten(self.tehai_state,len(self.furo_mentsu)+1)
			u_l=tehai_func.ukeire(self.tehai_state,len(self.furo_mentsu)+1)
			self.tehai_state[dahai.id]+=2
			u=0
			for i in u_l:
				u+=(4-self.environment_state[dahai.id])
			if cur_s>s or (cur_s==s and (cur_u<u or dahai.dora)):return(True,'pon',s,u,l)
			else:return (False,'pon',10,0,[])
			

		def daiminikan_check(dahai,cur_s,cur_u):
			return False,'daiminkan',10,0,[]

			if not dahai.id in self.can_furo_dic['daiminkan']:
				return False,'daiminkan',10,0,[]

		if ron_check(dahai):
			return (True,'ron',0)
		else:
			cur_s=tehai_func.Shanten(self.tehai_state,len(self.furo_mentsu))
			cur_u_l=tehai_func.ukeire(self.tehai_state,len(self.furo_mentsu))
			cur_u=0
			for i in cur_u_l:
				cur_u+=(4-self.environment_state[i])
			f_l=[daiminikan_check,pon_check,chi_check]
			boo,typ,shan,uke,li=False,0,10,0,[]
			for f in f_l:
				b,t,s,u,l=f(dahai,cur_s,cur_u)
				if b :
					if shan>s or (shan==s and uke<u):
						boo,typ,shan,uke,li=b,t,s,u,l
			return (boo,typ,li)

	def make_can_furo_dic(self,state,num_of_furoMentsu):
		self.can_furo_dic=tehai_func.can_furo_dic(state,num_of_furoMentsu)
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
		l.sort()
		self.furo_mentsu.append((typ,pai,ed_player_id,[self.tehai[i] for i in l]))
		j=0
		for i in l:
			self.tehai_state[self.tehai[i-j].id]-=1
			del self.tehai[i-j]
			j+=1
	def is_tempai(self):
		l=tehai_func.vectorize_pai_list(self.tehai)
		if tehai_func.Shanten(l)==0:
			return True
		else:
			return False
	