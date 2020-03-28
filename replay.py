import json
import pygame
import draw_replay
import taku_replay
import display_replay as display


file_name='../../tenho_paifu/paifu/2019scc20190101.json'
file=open(file_name)
data=json.load(file)

SCREEN_SIZE = (1400,750)  # 画面サイズ
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

#taku=taku_replay.taku(data)
display=display.display(data,screen)
#draw=draw_replay.draw(taku,screen)

pygame.display.update()# 画面を更新
print(data)
# ゲームループ
while True:
	# イベント処理
	for event in pygame.event.get():
		if event.type == pygame.QUIT:  # 終了イベント
			pygame.quit()
			#sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			update=display.button_controll(event.pos)
			if update:
				pygame.display.update()# 画面を更新
