import tokuten_cal
import numpy as np
import copy
class tokuten:
	def __init__(self,numOfPeople,mochiten,zerotobi,tsumibo_point,tenho=False,kiriageMangan=True):
		self.tokuten=[mochiten] * numOfPeople
		self.mochiten=mochiten
		self.zerotobi=zerotobi
		self.numOfPeople=numOfPeople
		self.tsumibo_point=tsumibo_point
		self.tenho=tenho
		self.kiriageMangan=kiriageMangan
		if numOfPeople==4:
			self.bappu=3000
		elif numOfPeople==3:
			self.bappu=1000#1人あたり
		elif numOfPeople==2:
			self.bappu=1000
		elif numOfPeople==1:
			self.bappu=1000
		self.cal=tokuten_cal.tokuten_cal(numOfPeople,tenho and numOfPeople==3,kiriageMangan)
	def top(self):
		#上家取りになってる
		return np.argmax(self.tokuten)
			

	def hora(self,han,fu,hora_id,oya_id,kyotaku,honba,hoju_id=None,tsumo=False):
		if tsumo:
			if hora_id==oya_id:
				daten,hoju_daten=self.tsumo_daten(han,fu,honba,True)
				for i in range(self.numOfPeople):
					if i==hora_id:
						self.tokuten[i]=self.tokuten[i]+daten+kyotaku
					else:
						self.tokuten[i]=self.tokuten[i]-hoju_daten
			else:
				daten,ko,oya=self.tsumo_daten(han,fu,honba,False)
				for i in range(self.numOfPeople):
					if i==hora_id:
						self.tokuten[i]=self.tokuten[i]+daten+kyotaku
					elif i==oya_id:
						self.tokuten[i]=self.tokuten[i]-oya
					else:
						self.tokuten[i]=self.tokuten[i]-ko
		else:
			if hora_id==oya_id:
				daten=self.deagari_daten(han,fu,honba,True)
				for i in range(self.numOfPeople):
					if i==hora_id:
						self.tokuten[i]=self.tokuten[i]+daten+kyotaku
					elif i==hoju_id:
						self.tokuten[i]=self.tokuten[i]-daten
			else:
				daten=self.deagari_daten(han,fu,honba,False)
				for i in range(self.numOfPeople):
					if i==hora_id:
						self.tokuten[i]=self.tokuten[i]+daten+kyotaku
					elif i==hoju_id:
						self.tokuten[i]=self.tokuten[i]-daten
	def ryukyoku(self,tempai_bool):
		tempai_num=tempai_bool.count(True)
		if self.numOfPeople==1:
			if tempai_bool[0]:
				self.tokuten[0]=self.tokuten[0]+self.bappu
				return
		elif tempai_num==0 or tempai_num==self.numOfPeople:
				return 
		if self.numOfPeople==4:
			ten=self.bappu//tempai_num
			for i in range(self.numOfPeople):
				if tempai_bool[i]:
					self.tokuten[i]=self.tokuten[i]+ten
				else:
					self.tokuten[i]=self.tokuten[i]-ten
		elif self.numOfPeople==3:
			for i in range(self.numOfPeople):
				if tempai_bool[i]:
					self.tokuten[i]=self.tokuten[i]+self.bappu//tempai_num
				else:
					self.tokuten[i]=self.tokuten[i]-self.bappu//(3-tempai_num)
		elif self.numOfPeople==2:
			ten=self.bappu
			for i in range(self.numOfPeople):
				if tempai_bool[i]:
					self.tokuten[i]=self.tokuten[i]+ten
				else:
					self.tokuten[i]=self.tokuten[i]-ten
	def end_score_correct(self,kaeshi_point,uma):
		if kaeshi_point==None:
			if self.numOfPeople>=3:kaeshi_point=self.mochiten+5000
			else:kaeshi_point=self.mochiten
		t=copy.copy(self.tokuten)
		#order=t.argsort() 上家優先にならない
		o=[0]*self.numOfPeople
		for i in range(self.numOfPeople):
			for j in range(i+1,self.numOfPeople):
				if t[i]<t[j]:
					o[j]+=1
				else:
					o[i]+=1
		order=[0]*self.numOfPeople
		for i in range(self.numOfPeople):
			for j in range(self.numOfPeople):
				if i==o[j]:
					order[i]=j
					break

		if uma==None:
			if self.numOfPeople==4:
				if self.tenho:
					l=[-70,0,20,50]
					for i in range(self.numOfPeople):
						j=order[i]
						t[j]=l[i]
				else:
					l=[-30000,-10000,10000,30000]
					for i in range(self.numOfPeople):
						j=order[i]
						t[j]-=kaeshi_point
						t[j]+=l[i]
						if i==self.numOfPeople-1:t[j]+=(kaeshi_point-self.mochiten)*self.numOfPeople

			elif self.numOfPeople==3:
				if self.tenho:
					l=[-70,0,70]
					for i in range(self.numOfPeople):
						j=order[i]
						self.t[j]=l[i]
				else:
					l=[-10000,-10000,0]
					for i in range(self.numOfPeople):
						if i<self.numOfPeople-1:
							j=order[i]
							if t[j]<kaeshi_point:
								t[j]-=(l[i]+kaeshi_point)
						else:
							t[j]-=kaeshi_point
			elif self.numOfPeople==2:
				pass
			else:
				pass
		else:
		
			for i in range(self.numOfPeople):
				j=order[i]
				t[i]-=kaeshi_point
				t[i]+=uma[j]
				if j==self.numOfPeople-1:t[i]+=(kaeshi_point-self.mochiten)*self.numOfPeople
		return t,order
	def tobi(self):
		if self.zerotobi==False:
			for ten in self.tokuten:
				if ten<0:
					return True
			return False
		else :
			for ten in self.tokuten:
				if ten<=0:
					return True
			return False
	#点移動
	#出あがり
	def deagari_daten(self,han,fu,honba,is_parent):
		if is_parent:
			func=self.cal.oya_deagari_daten
		else:
			func=self.cal.ko_deagari_daten
		daten=func(han,fu)+honba*self.tsumibo_point
		return daten
	#ツモ(打点,子の点移動,親の点移動)
	def tsumo_daten(self,han,fu,honba,is_parent):
		if is_parent:
			daten,ko=self.cal.oya_tsumo_daten(han,fu)
			oya=0
		else:
			daten,ko,oya=self.cal.ko_tsumo_daten(han,fu)
		if self.numOfPeople==4:
			ko=ko+honba*self.tsumibo_point//3
			oya=oya+honba*self.tsumibo_point//3
		elif self.numOfPeople==3:
			if self.tenho:
				ko=ko+honba*self.tsumibo_point//3
				oya=oya+honba*self.tsumibo_point//3
			else:#両方から同額
				ko=ko+honba*self.tsumibo_point
				oya=oya+honba*self.tsumibo_point
		else:
				ko=ko+honba*self.tsumibo_point
				oya=oya+honba*self.tsumibo_point


		if is_parent:
			if self.numOfPeople>=2:
				return ((self.numOfPeople-1)*ko,ko)
			else:
				return (ko,0)
		else:
			if self.numOfPeople>=2:
				return ((self.numOfPeople-2)*ko+oya,ko,oya)
			else:
				return (daten,ko,oya)
"""
############TEST	
num=2
tsumi=300
ten=False
t=tokuten(num,35000,False,tsumibo_point=tsumi,tenhoSamma=ten)
han=4
fu=40
print(t.tokuten)
hon=0
k=0
for o,a,h in [(0,0,1),(0,1,0)]:
	for tsu in [True,False]:
		for hon in [0,1]:		
					t.hora(han,fu,a,o,k,hon,h,tsu)
					print('tsu',tsu,', o:',o,', a:',a,', h:',h,', k:',k,', hon:',hon)
					print(t.tokuten)
					t.tokuten=[35000]*num
					print('')
"""
