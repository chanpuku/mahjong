import basic_replay as br
class taku:
	def __init__(self,data):
		self.data=data
		self.numOfPeople=data['game_info']['numOfPeople']
		self.numOfSet=data['game_info']['numOfSet']
		self.torikiri=data['game_info']['torikiri']
		self.hanahai=data['game_info']['hanahai']
		self.numOfTonpu=data['game_info']['numOfTonpu']
		self.mochiten=data['game_info']['mochiten']
		name=[data['game_info']['player_info'][i]['name'] for i in range(self.numOfPeople)]
		self.janshi=[br.janshi(self.mochiten,name=name[i])for i in range(self.numOfPeople)]
		self.chicha=self.data['kyoku'][0]['kyoku_info']['parent']
		self.set_first_last_of_yama()
	def set_first_last_of_yama(self):
		if self.numOfSet==2:
			first_last_of_yama=64
		elif self.numOfSet==3:
			first_last_of_yama=108
		elif self.numOfSet==4:
			first_last_of_yama=136
		first_last_of_yama-=self.numOfPeople*13
		if self.torikiri:
			first_last_of_yama-=6
		else:
			first_last_of_yama-=14
		self.first_last_of_yama=first_last_of_yama
	def setting_kyoku(self,i):
		data=self.data['kyoku'][i]['kyoku_info']
		self.current_kyoku_index=i
		self.kyoku=data['kyoku']
		self.honba=data['honba']
		self.kyotaku=data['kyotaku']
		score=data['score']
		self.parent=data['parent']
		self.dora_hyoji_id=[data['dora_hyoji_id']]
		self.dora={34,35,36}
		self.set_new_dora(data['dora_hyoji_id'])
		self.last_of_yama=self.first_last_of_yama
		for i in range(self.numOfPeople):
			self.janshi[i].kyoku_start((i+self.numOfPeople-self.parent)%self.numOfPeople)
			self.janshi[i].mochiten=score[i]
		self.haipai_setting(data['haipai'])
		self.turn=self.parent
		self.complete_dahai=False
		self.furo=(-1,-1,-1)#[type,id,from_id]
		self.state='tsumoban'#[kiriban,tsumoban,kyoku_end]

	"""
	得点移動用
	setting_kyokuでやる
	def kyoku_end(self,data):
		score_move=data['score_move']
		for i in range(self.numOfPeople):
			self.janshi[i].mochiten+=score_move[2*i]
	"""
	def kyoku_start(self,data):
		pass
	def next(self,data):
		if data['type']=='TSUMO':
			player_id=data['player_id']
			pai_id=data['pai_id']
			self.janshi[player_id].tsumo(pai_id)
			self.last_of_yama-=1
			self.turn=player_id
			self.state='kiriban'
			self.janshi[(player_id-1)%self.numOfPeople].tehai.sort()#ツモ後の上家と鳴き後の鳴き後の泣かせた鳴かせた人	
			
		elif data['type']=='DAHAI':
			player_id=data['player_id']
			pai_id=data['pai_id']
			tsumogiri=data['tsumogiri']
			self.janshi[player_id].dahai(pai_id,tsumogiri)
			self.state='tsumoban'
		elif data['type']=='REACH':
			if data['step']==1:
				player_id=data['player_id']
				self.janshi[player_id].reach_preparation=True
			if data['step']==2:
				player_id=data['player_id']
				self.janshi[player_id].reach=True
		elif data['type']=='NAKI':
			player_id=data['player_id']
			type2=data['type2']
			from_player_id=data['from_player_id']
			self.janshi[from_player_id].tehai.sort()
			pai_id=data['pai']
			#l=data['reveal_pai_list']#kakanには無いため各分岐で
			self.furo=(type2,player_id,from_player_id)
			self.turn=player_id

			if type2=='nuki':
				self.janshi[player_id].nuki(pai_id)
				self.state='tsumoban'
			elif type2=='ankan':
				self.janshi[player_id].ankan(pai_id)
				self.state='tsumoban'
			elif type2=='kakan':
				self.janshi[player_id].kakan(pai_id)
				self.state='tsumoban'
			elif type2=='daiminkan':
				l=data['reveal_pai_list']
				self.janshi[from_player_id].sutehai[-1].ed_furo_id=player_id
				self.janshi[player_id].furo('daiminkan',pai_id,from_player_id,l)
				self.state='tsumoban'
			else:
				l=data['reveal_pai_list']
				self.janshi[from_player_id].sutehai[-1].ed_furo_id=player_id
				self.janshi[player_id].furo(type2,pai_id,from_player_id,l)
				self.state='kiriban'
		elif data['type']=='DORA':
			self.dora_hyoji_id.append(data['new_dora'])
			self.set_new_dora(data['new_dora'])
		elif data['type']=='AGARI':
			pass
	def back(self,data):
		pass
	def haipai_setting(self,haipai_list):
		for i in range(self.numOfPeople):
			haipai=haipai_list[i]
			for j in range(len(haipai)):
				self.janshi[i].tehai.append(br.pai(0,0,id=haipai[j]))
			self.janshi[i].tehai.sort()
	
	def set_new_dora(self,dora_hyoji_id):
		if dora_hyoji_id>33:
			d=(dora_hyoji_id-34)*9+5
			self.dora.add(d)
		else:
			t=(dora_hyoji_id//9)
			d=t*9+(dora_hyoji_id%9+1)%9
			self.dora.add(d)



	
