# -*- coding: utf-8 -*-
import random
import basic
import tokuten
import numpy as np
import json
import copy
import environment
class taku:
	def set_yama(self,numOfPeople,numOfAkadora,numOfSet,torikiri,hanahai):
		pointOfDoraHyoji=[5+hanahai]
		#１人、２人麻雀用
		if numOfSet==-1:
			self.yama=basic.yama(numOfPeople,numOfAkadora,pointOfDoraHyoji)
		else:
			self.yama=basic.yama(numOfSet,numOfAkadora,pointOfDoraHyoji)
		#debug
		self.yama.make([27,28,27,28,28,27],tsumo_id_list=[30,31,27,28])

		#カンによるlast_of_yamaの変化はカンの方で
		if numOfPeople==1:
			self.last_of_yama=18
		else:
			if torikiri:
				self.last_of_yama=len(self.yama)-13*numOfPeople-(4+hanahai+2)
			else:
				self.last_of_yama=len(self.yama)-13*numOfPeople-14
		self.dora=self.yama.dora
	def set_haipai(self,numOfPeople,yama,parent):
		l=[[] for i in range(numOfPeople)]
		j=parent
		for i in range(13*numOfPeople):
			l[j].append(yama.pop())
			j=(j+1)%numOfPeople
		for i in range(numOfPeople):
			self.janshi[i].tehai=l[i]
			self.janshi[i].dora_hyoji=[self.yama.yama[self.yama.dora_hyoji[0]]]
			self.janshi[i].getting_haipai()
	def kan_happen(self):
		self.kan_times+=1
		pai=self.yama.kan()
		self.environment.update_dora()
		return pai
	def __init__(self,numOfPeople,numOfAkadora,numOfSet=-1,numOfKyoku=None,numOfTonpu=2,mochiten=25000,tenpai_rentyan=True,
				chicha=None,daburon=True,tobi_end=True,zerotobi=False,torikiri=False,hanahai=0,tsumibo_point=300,oyaken_kamityadori=False,
				tenho=False,kaeshi_point=None,uma=None,visual=True,saifu=False,):
		#self.state=[geme_end,kyoku_start,kyoku_end,tsumo_turn_start,action,dahai_check,tsumo_turn_end,finished
		
		self.numOfPeople=numOfPeople
		self.numOfAkadora=numOfAkadora
		self.numOfSet=numOfSet
		self.torikiri=torikiri
		self.hanahai=hanahai
		self.numOfKyoku=numOfPeople if numOfKyoku==None else numOfKyoku
		self.numOfTonpu=numOfTonpu
		self.tenpai_rentyan=tenpai_rentyan
		self.daburon=daburon
		self.chicha=chicha
		self.tobi_end=tobi_end
		self.mochiten=mochiten
		self.tsumibo_point=tsumibo_point
		self.zerotobi=zerotobi
		self.oyaken_kamityadori=oyaken_kamityadori
		self.tenho=tenho
		self.kaeshi_point=kaeshi_point
		self.uma=uma
		self.can_chi=self.numOfPeople==4

		self.saifu=saifu
		self.janshi=[basic.janshi(self.mochiten) for i in range(numOfPeople)]
		#paifu
		self.json_file=open('paifu/paifu.json' , 'w')
		self.paifu={'game_info':{},'kyoku':[],'end_info':{}}
		self.paifu['game_info']['numOfPeople']=self.numOfPeople
		self.paifu['game_info']['numOfAkadora']=self.numOfAkadora
		self.paifu['game_info']['numOfSet']=self.numOfSet
		self.paifu['game_info']['torikiri']=self.torikiri
		self.paifu['game_info']['hanahai']=self.hanahai
		self.paifu['game_info']['numOfKyoku']=self.numOfKyoku
		self.paifu['game_info']['numOfTonpu']=self.numOfTonpu
		self.paifu['game_info']['tenpai_rentyan']=self.tenpai_rentyan
		self.paifu['game_info']['daburon']=self.daburon
		self.paifu['game_info']['chicha']=self.chicha
		self.paifu['game_info']['tobi_end']=self.tobi_end
		self.paifu['game_info']['mochiten']=self.mochiten
		self.paifu['game_info']['tsumibo_point']=self.tsumibo_point
		self.paifu['game_info']['zerotobi']=self.zerotobi
		self.paifu['game_info']['oyaken_kamityadori']=self.oyaken_kamityadori


		#drawでエラーが出ないために初期化してる、結局するから処理自体はしてもしなくても一緒<-state=game_startの方をなくした
		
		#game初め
		self.game_start()
		
		#局初め
		self.kyoku_start()
	def game_start(self):
		self.tokuten=tokuten.tokuten(self.numOfPeople,self.mochiten,self.zerotobi,self.tsumibo_point)
		self.kyoku=1
		self.honba=0
		self.kyotaku=0
		if self.chicha==None:
			self.chicha=random.randint(0,self.numOfPeople-1)
		self.parent=self.chicha
		self.state='kyoku_start'
		self.environment=environment.environment(self)
		
	def game_end(self):
		if self.kyotaku>0:
			top=self.tokuten.top()
			self.tokuten.tokuten[top]=self.tokuten.tokuten[top]+self.kyotaku
		#paifu
		t,o=self.tokuten.end_score_correct(self.kaeshi_point,self.uma)
		l=[]
		for i in range(self.numOfPeople):
			d={}
			j=self.numOfPeople-i-1
			k=o[j]
			d['order'],d['player_id'],d['score'],d['finish_point']=i+1,k,self.tokuten.tokuten[k],t[k]
			l.append(d)

		self.paifu['end_info']['score']=l
		if self.saifu:
			json.dump(self.paifu, self.json_file, ensure_ascii=False, indent=4,separators=(',', ': '))
			#json.dump(self.paifu, self.json_file, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
		self.state='finished'
	def kyoku_start(self):
		for i in range(self.numOfPeople):
			wind=(i-self.parent)%self.numOfPeople
			self.janshi[i].kyoku_start(wind)

		self.set_yama(self.numOfPeople,self.numOfAkadora,self.numOfSet,self.torikiri,self.hanahai)
		self.set_haipai(self.numOfPeople,self.yama.yama,self.parent)
		self.turn = self.parent
		self.ryukyoku=False
		self.kan_times=0
		self.environment.kyoku_start()
		self.state='tsumo_turn_start'
		#全体を通して使う
		self.furo_happen=False
		self.ed_furo_id=-1#泣かれたひとのid
		self.furo_id=-1#泣いた人のid
		self.furo_type=None #[tsumo,ron,pon,chi,ankan,kakan,daiminkan]
		self.hora_list=[]#[hora_id,hoju_id,han,fu]
		self.kamitya_hora_id=-1
		self.dahai=-1
		self.tsumo=0
		#paifu
		self.temp_paifu={'info':{},'moda':[],'end':{}}
		self.temp_paifu['info']={'kyoku':self.kyoku,'honba':self.honba,'kyotaku':self.kyotaku,'oya':self.parent}
		self.temp_paifu['info']['dora_hyoji']=self.yama.yama[self.yama.dora_hyoji[0]].name
		self.temp_paifu['info']['haipai']=[[pai.name for pai in self.janshi[i].tehai] for i in range(self.numOfPeople)]
		self.temp_paifu['info']['score']=copy.copy(self.tokuten.tokuten)
		self.temp_paifu['end']['renchan']=True

	def kyoku_end(self):
		if self.ryukyoku:
			tenpai_bool=[jan.is_tempai() for jan in self.janshi]
			self.tokuten.ryukyoku(tenpai_bool)
			rentyan=self.janshi[self.parent].is_tempai() and self.tenpai_rentyan
			self.honba=self.honba+1

			#paifu
			self.temp_paifu['end']['frag']='ryukyoku'
			self.temp_paifu['end']['tempai']=[self.janshi[i].is_tempai() for i in range(self.numOfPeople)]
			if not rentyan:
				self.kyoku=self.kyoku+1
				self.parent=(self.parent+1)%self.numOfPeople
				#paifu
				self.temp_paifu['end']['renchan']=False
		else:
			c=self.numOfPeople*2
			for hora_id,hoju_id,_,_ in self.hora_list:
				if hoju_id==-1:
					self.kamitya_hora_id=hora_id
					break
				if hora_id<hoju_id:
					d=hora_id+self.numOfPeople
				else:d=hora_id
				if c>d:
					c=d
					self.kamitya_hora_id=hora_id

			for hora_id,hoju_id,han,fu in self.hora_list:
				kyotaku,honba=0,0
				if hora_id==self.kamitya_hora_id:
					kyotaku,honba=self.kyotaku,self.honba
				if hoju_id==-1:
					self.tokuten.hora(han,fu,hora_id,self.parent,kyotaku,honba,tsumo=True)
				else:
					self.tokuten.hora(han,fu,hora_id,self.parent,kyotaku,honba,hoju_id=hoju_id)
			rentyan=self.parent==self.kamitya_hora_id
			self.kyotaku=0
			#paifu
			self.temp_paifu['end']['frag']='hora'
			l=[]
			for t in self.hora_list:
				dic={}
				dic['hora_id'],dic['hoju_id'],dic['han'],dic['fu']=t
				l.append(dic)
			self.temp_paifu['end']['hora_list']=l
			if rentyan:
				self.honba=self.honba+1
			else:
				self.kyoku=self.kyoku+1
				self.honba=0
				self.parent=(self.parent+1)%self.numOfPeople
				#paifu
				self.temp_paifu['end']['renchan']=False
		
		can_finish=self.kyoku>self.numOfKyoku*self.numOfTonpu
		if self.tobi_end:
			can_finish=can_finish or self.tokuten.tobi()
		if not can_finish:
			self.state='kyoku_start'
		else:
			self.state='game_end'
		#paifu
		self.temp_paifu['end']['score']=copy.copy(self.tokuten.tokuten)
		self.paifu['kyoku'].append(self.temp_paifu)
	def tsumo_turn_start(self,kan=False):
		if self.last_of_yama==0:
			self.ryukyoku=True
			self.state='kyoku_end'
		else:
			kan= self.furo_type =='ankan' or self.furo_type =='kakan' or self.furo_type =='daiminkan'
			jan=self.janshi[self.turn]
			if kan:
				pai=self.kan_happen()
				self.tsumo=jan.tsumo(self.yama.yama,pai=pai)
			else:self.tsumo=jan.tsumo(self.yama.yama)
			self.last_of_yama=self.last_of_yama-1
			self.environment.update_tsumo()
			self.state='tsumo_action'
	def tsumo_action(self):
		
		if self.furo_happen:
			if self.furo_type=='kakan' or self.furo_type=='ankan' or self.furo_type =='daiminkan':
				typ,result=self.janshi[self.turn].action(self.environment,tsumo_pai=self.tsumo)
			else:#’pon','chi'
				typ,result=self.janshi[self.turn].action(self.environment,tsumo_pai=self.tsumo,furo=True)
		else:
			typ,result=self.janshi[self.turn].action(self.environment,tsumo_pai=self.tsumo)
		self.furo_happen=False
		self.ed_furo_id=-1#泣かれたひとのid
		self.furo_id=-1#泣いた人のid
		self.furo_type=None #[tsumo,ron,pon,chi,ankan,kakan,daiminkan]
		if typ=='tsumo':
			self.furo_happen=True#泣かれたひとのid
			self.furo_id=self.turn
			self.ed_furo_id=-1#泣かれたひとのid
			self.furo_type='tsumo'
			self.kamitya_hora_id=self.turn
			self.hora_list.append((self.turn,-1,result[0],result[1]))
			self.state='kyoku_end'
		elif typ=='ankan':
			self.furo_happen=True#泣かれたひとのid
			self.furo_id=self.turn
			self.ed_furo_id=-1#泣かれたひとのid
			self.furo_type='ankan' 
			#self.kan_times+=1
			self.environment.update_furo(self.turn,typ,result,self.janshi[self.turn].furo_mentsu[-1][-1])
			self.state='tsumo_turn_start'
		elif typ=='kakan':
			self.furo_happen=True#泣かれたひとのid
			self.furo_id=self.turn
			self.ed_furo_id=-1#泣かれたひとのid
			self.furo_type='kakan'
			self.dahai=result
			self.environment.update_furo(self.turn,typ,result.correct_id,self.janshi[self.turn].furo_mentsu[-1][-1])
			#self.kan_times+=1
			self.state='dahai_check'
		else:
			self.dahai=result
			self.environment.update_dahai(self.turn,result.correct_id)
			self.state='dahai_check'
		
	def dahai_check(self):
		happen_typ=''
		player_id=-1
		li=[]
		for i in range(self.numOfPeople):
			if i==self.turn:continue
			b,typ,l=self.janshi[i].furo_check(self.dahai,self.can_chi and i==(self.turn+1)%self.numOfPeople,self.environment,chankan=self.furo_type=='kakan')
			if b:
				if typ=='ron':
					happen_typ='ron'
					han,fu=self.tokuten.cal.cal_han_and_fu(self.janshi[i].tehai,self.janshi[i].furo_mentsu,self.dahai,False)
					self.hora_list.append((i,self.turn,han,fu))
				elif happen_typ=='ron':
					continue
				elif typ=='pon':
					happen_typ='pon'
					player_id=i 
					li=l
				elif typ=='daiminkan':
					happen_typ='daiminkan'
					player_id=i 
					li=l
				elif typ=='chi' and happen_typ=='':
					happen_typ='chi'
					player_id=i 
					li=l
		if happen_typ=='ron':
			self.furo_happen=True#泣かれたひとのid
			#self.furo_id=player_id
			self.ed_furo_id=self.turn#泣かれたひとのid
			self.furo_type='ron' 
			self.dahai.ed_furo_id=player_id
			self.dahai.ed_furo_type=happen_typ
			self.state='kyoku_end'
		elif happen_typ=='':
			self.state='tsumo_turn_end'
		else:	
			self.janshi[player_id].furo(happen_typ,self.dahai,self.turn,li)
			self.furo_happen=True
			self.furo_id=player_id
			self.ed_furo_id=self.turn#泣かれたひとのid
			self.furo_type=happen_typ
			self.dahai.ed_furo_id=player_id
			self.dahai.ed_furo_type=happen_typ
			self.environment.update_furo(self.furo_id,happen_typ,self.dahai.correct_id,self.janshi[player_id].furo_mentsu[-1][-1])
			self.state='tsumo_turn_end'
	def tsumo_turn_end(self):
		if self.furo_type=='pon'or self.furo_type=='chi':
			self.turn=self.furo_id
			self.state='tsumo_action'
		elif self.furo_type=='daiminkan':
			self.turn=self.furo_id
			self.state='tsumo_turn_start'
		elif self.furo_type=='kakan':#チャンカンチェックが入る
			self.turn=self.furo_id
			"""多分いらないしコメントにしてる
			self.furo_happen=False
			self.ed_furo_id=-1#泣かれたひとのid
			self.furo_id=-1#泣いた人のid
			self.furo_type=None #[tsumo,ron,pon,chi,ankan,kakan,daiminkan]
			"""
			self.state='tsumo_turn_start'
		#それ以外のfuroはここにこない
		else:
			self.turn=(self.turn+1)%self.numOfPeople
			self.state='tsumo_turn_start'

	def controll(self):
		if self.state=='game_end':
			self.game_end()
		elif self.state=='kyoku_start':
			self.kyoku_start()
		elif self.state=='kyoku_end':
			self.kyoku_end()
		elif self.state=='tsumo_turn_start':
			self.tsumo_turn_start()
		elif self.state=='tsumo_action':
			self.tsumo_action()
		elif self.state=='dahai_check':
			self.dahai_check()
		elif self.state=='tsumo_turn_end':
			self.tsumo_turn_end()
		elif self.state=='finished':
			pass
		else:
			print('error')
	def undo(self):
		pass



