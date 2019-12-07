import numpy as np
class environment:
    def __init__(self,taku):
        self.taku=taku
        self.game_kind=None
        self.chicha=self.taku.chicha
        self.numOfPeople=self.taku.numOfPeople
        self.numOfSet=self.taku.numOfSet
        self.mochiten=self.taku.mochiten
        self.tenpai_rentyan=self.taku.tenpai_rentyan
        self.daburon=self.taku.daburon
        self.tobi_end=self.taku.tobi_end
        self.zerotobi=self.taku.zerotobi
        self.hanahai=self.taku.hanahai
        self.tsumibo_point=self.taku.tsumibo_point
        self.oyaken_kamityadori=self.taku.oyaken_kamityadori
        self.tenho=self.taku.tenho
        self.kaeshi_point=self.taku.kaeshi_point
        self.uma=self.taku.uma
        self.janshi=self.taku.janshi
        self.KIND_OF_PAI=34
        self.KIND_OF_PAI_NOMAL=37
        self.state=np.zeros(self.KIND_OF_PAI_NOMAL)
    def kyoku_start(self):
        self.field_wind=self.taku.field_wind
        self.kyoku=self.taku.kyoku
        self.honba=self.taku.honba
        self.kyotaku=self.taku.kyotaku
        self.dora_hyoji=self.taku.dora_hyoji
        self.dora=self.taku.dora
        self.parent=self.taku.parent
        self.sutehai=[self.janshi[i].sutehai for i in range(self.numOfPeople)]
        self.furo_mentsu=[self.janshi[i].furo_mentsu for i in range(self.numOfPeople)]
        self.state=np.zeros(self.KIND_OF_PAI_NOMAL)
        
    def update_dora(self):
        self.state[self.dora_hyoji[-1]]+=1
    
    #mutableだから必要ない気がする
    def update_dahai(self,player_id):
        self.janshi[player_id].sutehai=self.taku.janshi[player_id]
    
    #mutableだから必要ない気がする
    def update_furo(self):
        pass
            

