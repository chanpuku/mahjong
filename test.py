import pygame

SCREEN_SIZE = (1400,750)  # 画面サイズ
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.update()# 画面を更新

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        super().__init__()
        #self.rect = (50,100,150,200)
player=Player()
# ゲームループ
while True:
	# イベント処理
	for event in pygame.event.get():
		if event.type == pygame.QUIT:  # 終了イベント
			pygame.quit()
			#sys.exit()
		
