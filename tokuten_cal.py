import math 
import mahjong
class tokuten_cal:
	def __init__(self,numOfPeople,tenhoSamma,kiriageMangan):
		self.numOfPeople=numOfPeople
		self.tenhoSamma=tenhoSamma
		self.kiriageMangan=kiriageMangan
	def cal_han_and_fu(self,tehai,furo_mentsu,agarihai,tsumo):
		han=self.cal_han(tehai,furo_mentsu,agarihai,tsumo)
		fu=self.cal_fu(tehai,furo_mentsu,agarihai,tsumo) if han<5 else 40
		return (han,fu)
	def cal_han(self,tehai,furo_mentsu,agarihai,tsumo):
		return 4
	def cal_fu(self,tehai,furo_mentsu,agarihai,tsumo):
		return 40
	def ko_deagari_daten(self,han,fu):
		basic=math.ceil((fu*2**(han+2)*4)/100)*100
		mangan=8000
		if self.kiriageMangan:
			mangan=7700
		if basic<mangan:
			return basic
		elif han<=5:
			return 8000
		elif han<=7:
			return 12000
		elif han<=10:
			return 16000
		elif han<=12:
			return 24000
		else:
			return 32000

	def oya_deagari_daten(self,han,fu):
		basic=math.ceil((fu*2**(han+2)*6)/100)*100
		mangan=12000
		if self.kiriageMangan:
			mangan=11600
		if basic<mangan:
			return basic
		else:
			return self.ko_deagari_daten(han,fu)//2*3

	def ko_tsumo_daten(self,han,fu):
		if self.numOfPeople==4:
			return self.four_ko_tsumo_daten(han,fu)
		elif self.numOfPeople==3:
			if self.tenhoSamma:
				_,ko,oya=self.four_ko_tsumo_daten(han,fu)
				return (ko+oya,ko,oya)
			else:
				daten=self.ko_deagari_daten(han,fu)
				return self.three_tsumo_daten(daten)
		elif self.numOfPeople==2:
			oya=self.ko_deagari_daten(han,fu)
			return (oya,0,oya)
		elif self.numOfPeople==1:
			oya=self.ko_deagari_daten(han,fu)
			return (oya,oya,0)
	def oya_tsumo_daten(self,han,fu):
		if self.numOfPeople==4:
			return self.four_oya_tsumo_daten(han,fu)
		elif self.numOfPeople==3:
			if self.tenhoSamma:
				_,ko=self.four_oya_tsumo_daten(han,fu)
				return (ko*2,ko)
			else:
				daten=self.oya_deagari_daten(han,fu)
				daten=math.ceil(daten/1000)*1000
				ko=math.ceil(daten/2/1000)*1000
				return (ko*2,ko)
		elif self.numOfPeople==2:
			ko=self.oya_deagari_daten(han,fu)
			return (ko,ko)
		elif self.numOfPeople==1:
			p=self.oya_deagari_daten(han,fu)
			return (p,p)
	def four_ko_tsumo_daten(self,han,fu):
		basic=fu*2**(han+2)
		mangan=2000
		if self.kiriageMangan:
			mangan=1920
		if basic<mangan:
			ko=math.ceil(basic/100)*100
			oya=math.ceil(basic*2/100)*100
			return (ko*2+oya,ko,oya)
		else:
			p=self.ko_deagari_daten(han,fu)
			return (p,p//4,p//2)
	
	def four_oya_tsumo_daten(self,han,fu):
		basic=fu*2**(han+2)
		mangan=2000
		if self.kiriageMangan:
			mangan=1920
		if basic<mangan:
			ko=math.ceil(basic*2/100)*100
			return (ko*3,ko)
		else:
			p=self.oya_deagari_daten(han,fu)
			return (p,p//3)
			
	def three_tsumo_daten(self,daten):
		daten=math.ceil(daten/1000)*1000
		if daten<=4000:
			ko=1000
		elif daten<=7000:
			ko=2000
		elif daten==8000:
			ko=3000
		elif daten==12000:
			ko=4000
		elif daten==16000:
			ko=6000
		elif daten==24000:
			ko=8000
		elif daten==32000:
			ko=11000
		oya=daten-ko
		if oya<ko:
			oya=ko
		return (ko+oya,ko,oya)
"""
###TEST###
t=False
k=True
num=2
c=tokuten_cal(num,tenhoSamma=t,kiriageMangan=k)
fu=[20,25,30,40,50,60,70,80,90,100,110]
func=c.ko_tsumo_daten
for han in range(1,14):
	if han<4:
		for f in fu:
			print(han,f,'  :  ',func(han,f))
	elif han==4:
		for i in range(5):
			f=fu[i]
			print(han,f,'  :  ',func(han,f))
	else:
		f=20
		print(han,f,'  :  ',func(han,f))
"""
