# -*- coding: utf-8 -*-
import random
import pygame
import tehai_func
import numpy as np
import basic
#class agent :
class agent (basic.janshi):
	def __init__(self):
		self.tehai=[]
		self.sutehai=[]
		self.tenpai=False
		self.reach=False
	def get_haipai(self,yama):
		self.tehai=yama.yama[-13:]
		self.tehai.sort()
		del yama.yama[-13:]
	def tsumo(self,yama,kan=False):
		pai=yama.pop()
		#なんらかの判定
		self.tehai.append(pai)
		return pai
	def action(self,hora=False,tsumo_pai=0):
		if  hora:
			rd=self.hora_dahai()
			return ('dahai',rd)
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
				rd=self.dahai(tsumo_pai)
				return ('dahai',rd)
	def dahai(self,tsumo_pai):
		#打牌ロジック
		l=tehai_func.vectorize_pai_list(self.tehai)
		s,si=10,-1
		for i in range(len(self.tehai)):
			lc=np.copy(l)
			lc[self.tehai[i].id]=lc[self.tehai[i].id]-1
			a=tehai_func.Shanten(lc)
			if a<s:
				s,si=a,i
			elif a==s and self.tehai[i].typ=='z':
				s,si=a,i
		pai=self.tehai[si]
		self.sutehai.append(pai)
		del self.tehai[si]
		self.tehai.sort()
		return pai
	def hora_dahai(self):
		return -1
	def kakan_check(self,tsumo_pai):
		return False,-1
	def ankan_check(self,tsumo_pai):
		return False,-1
	def tsumo_check(self,tsumo_pai):
		han,hu=4,30
		l=tehai_func.vectorize_pai_list(self.tehai)
		if tehai_func.Shanten(l)==-1:
			return True,(han,hu)
		return False,(han,hu)

	def hora_check(self,dahai):
		return False

