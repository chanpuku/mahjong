import datetime
import copy 
import json
class paifu_make:
	def __init__(self,saifu):
		self.saifu=saifu
		if saifu:
			self.paifu={'game_info':{},'kyoku':[],'game_end_info':{}}
			self.file_name=str(datetime.datetime.today())
	def game_start(self,taku):
		if not self.saifu:return
		self.paifu['game_info']['numOfPeople']=taku.numOfPeople
		self.paifu['game_info']['numOfAkadora']=taku.numOfAkadora
		self.paifu['game_info']['numOfSet']=taku.numOfSet
		self.paifu['game_info']['torikiri']=taku.torikiri
		self.paifu['game_info']['hanahai']=taku.hanahai
		self.paifu['game_info']['numOfKyoku']=taku.numOfKyoku
		self.paifu['game_info']['numOfTonpu']=taku.numOfTonpu
		self.paifu['game_info']['tenpai_renchan']=taku.tenpai_renchan
		self.paifu['game_info']['daburon']=taku.daburon
		self.paifu['game_info']['chicha']=taku.chicha 
		self.paifu['game_info']['tobi_end']=taku.tobi_end
		self.paifu['game_info']['mochiten']=taku.mochiten
		self.paifu['game_info']['tsumibo_point']=taku.tsumibo_point
		self.paifu['game_info']['zerotobi']=taku.zerotobi
		self.paifu['game_info']['oyaken_kamityadori']=taku.oyaken_kamityadori
	def game_end(self,taku):
		if not self.saifu:return
		json_file=open('paifu/'+self.file_name+'.json' , 'w')
		t,o=taku.tokuten.end_score_correct(taku.kaeshi_point,taku.uma)
		l=[]
		for i in range(taku.numOfPeople):
			d={}
			j=taku.numOfPeople-i-1
			k=o[j]
			d['order'],d['player_id'],d['score'],d['finish_point']=i+1,k,taku.tokuten.tokuten[k],t[k]
			l.append(d)

		self.paifu['game_end_info']['score']=l
		json.dump(self.paifu, json_file, ensure_ascii=False, indent=4,separators=(',', ': '))
		#json.dump(self.paifu, json_file, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
	def kyoku_start(self,taku):
		if not self.saifu:return
		self.temp_paifu={'kyoku_info':{},'moda':[],'kyoku_end_info':{}}
		self.temp_paifu['kyoku_info']={'kyoku':taku.kyoku,'honba':taku.honba,'kyotaku':taku.kyotaku,'parent':taku.parent}
		self.temp_paifu['kyoku_info']['dora_hyoji']=taku.yama.yama[taku.yama.dora_hyoji[0]].name
		self.temp_paifu['kyoku_info']['haipai']=[[pai.name for pai in taku.janshi[i].tehai] for i in range(taku.numOfPeople)]
		self.temp_paifu['kyoku_info']['score']=copy.copy(taku.tokuten.tokuten)
	def kyoku_end(self,ryukyoku,renchan,taku):
		if not self.saifu:return
		if ryukyoku:
			self.temp_paifu['kyoku_end_info']['frag']='Ryukyoku'
			self.temp_paifu['kyoku_end_info']['renchan']=renchan
			self.temp_paifu['kyoku_end_info']['tempai']=[taku.janshi[i].is_tempai() for i in range(taku.numOfPeople)]
		else:
			self.temp_paifu['kyoku_end_info']['frag']='Agari'
			self.temp_paifu['kyoku_end_info']['renchan']=renchan
			l=[]
			for t in taku.hora_list:
				dic={}
				dic['hora_id'],dic['hoju_id'],dic['han'],dic['fu']=t
				l.append(dic)
			self.temp_paifu['kyoku_end_info']['hora_list']=l
		#paifu
		self.temp_paifu['kyoku_end_info']['score']=copy.copy(taku.tokuten.tokuten)
		self.paifu['kyoku'].append(self.temp_paifu)
			
	def tusmo(self):
		if not self.saifu:return
		pass
	def dahai(self):
		if not self.saifu:return
		pass
	def naki(self):
		if not self.saifu:return
		pass
	def agari(self):
		if not self.saifu:return
		pass
