import basic
class taku:
	def __init__(self,data):
		self.data=data
		self.numOfPeople=data['game_info']['numOfPeople']
		self.janshi=[basic.janshi()for i in range(self.numOfPeople)]
	def kyoku_setting(self,i):
		pass
	def next(self):
		pass
	def back(self):
		pass

	
