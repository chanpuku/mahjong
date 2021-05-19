import basic
class janshi(basic.janshi):
	def _init__(self,mochiten,name=None):
		super(janshi,self).__init__(mochiten,name=name)
		self.tsumo_pai=None
		self.dahai_point=13
		self.reach_preparation=False
	def kyoku_start(self, wind):
		self.dahai_point=13
		self.reach_preparation=False
		super().kyoku_start(wind)
	def tsumo(self,pai_id):
		self.tehai.append(basic.pai(0,0,id=pai_id))
	def dahai(self,pai_id,tsumogiri):
		if tsumogiri:
			pai=self.tehai[-1]
			del self.tehai[-1]
			self.dahai_point=-1
			pai.tsumogiri=True
		else:
			for i in range(len(self.tehai)):
				if self.tehai[i].correct_id==pai_id:
					k=i
					break
			pai=self.tehai[k]
			del self.tehai[k]
			self.dahai_point=k
		if self.reach_preparation:
			pai.reach_declaration=True
			self.reach_preparation=False
		self.sutehai.append(pai)
		
		#self.tehai.sort()
	def furo(self,typ,pai_id,ed_player_id,l):
		#'kakan','ankan'はここに来ない
		pai=basic.pai(0,0,id=pai_id)
		self.furo_mentsu.append([typ,pai,ed_player_id,[basic.pai(0,0,id=i) for i in l]])
		j=0
		del_list=[]
		for i in range(len(self.tehai)):
			if self.tehai[i].correct_id==l[j]:
				del_list.append(i)
				j+=1
				if j>=len(l):break
		j=0
		for i in del_list:
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
		for i in range(len(self.furo_mentsu)):
			if self.furo_mentsu[i][1].id==pai.id:
				self.furo_mentsu[i][0]='kakan'
				self.furo_mentsu[i][3].append(pai)
				break
	def ankan(self,id):
		l=[]
		j=0
		for i in range(len(self.tehai)):
			if self.tehai[i-j].id==id:
				l.append(self.tehai[i-j])
				pai=self.tehai.pop(i-j)
				j+=1
		self.furo_mentsu.append(['ankan',pai,-1,l])
	
	def nuki(self,id):
		l=[]
		for i in range(len(self.tehai)):
			if self.tehai[i].id==id:
				l.append(self.tehai[i])
				pai=self.tehai.pop(i)
				break
		self.furo_mentsu.append(['nuki',pai,-1,l])
		


class pai(basic.pai):
	pass


