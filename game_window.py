


def main():
	import pygame
	import basic
	import taku
	import sys
	import time
	import draw
	import agent
	SCREEN_SIZE = (1400,750)  # 画面サイズ
 
	#Pygameを初期化
	pygame.init()
	# SCREEN_SIZEの画面を作成
	screen = pygame.display.set_mode(SCREEN_SIZE)
	# タイトルバーの文字列をセット
	pygame.display.set_caption('ウィンドウの作成')

	#init
	#卓の設定
	numOfPeople=2
	numOfAkadora=1
	numOfSet=2

	#視覚用
	sleep_time=0
	sleep_time_kyoku_end=3
	#import prototype
	#agent=prototype.agent()
	taku=taku.taku(numOfPeople,numOfAkadora,numOfTonpu=1,numOfSet=numOfSet,torikiri=True,saifu=True)
	draw_controll=draw.draw_controll(taku,screen)
	pygame.display.update()# 画面を更新
	state='run'
	kyoku_end_draw_first=True
	# ゲームループ
	while True:
		# イベント処理
		for event in pygame.event.get():
			if event.type == pygame.QUIT:  # 終了イベント
				pygame.quit()
				return
				#sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				state=draw_controll.button_controll(event.pos)
				draw_controll.debug(x=len(pygame.event.get()))
				
				if state=='run':
					pass
				elif state=='stop':
					pass
				elif state=='undo':
					taku.undo()
				elif state=='new_game':
					taku.__init__(numOfPeople,numOfAkadora,numOfTonpu=1,numOfSet=numOfSet,torikiri=True,saifu=True)
					state='run'
		
		if not kyoku_end_draw_first:
			time.sleep(sleep_time_kyoku_end)
		if state=='run':
			if taku.state=='finished':
				#draw_controll.draw_game_end()
				#time.sleep(sleep_time_kyoku_end)
				state=='stop'
			elif taku.state=='kyoku_end' and kyoku_end_draw_first:
				taku.controll()
				draw_controll.draw_kyoku_end()
				kyoku_end_draw_first=False
			else:
				taku.controll()
				draw_controll.update_display()
				kyoku_end_draw_first=True

		#常にする
		draw_controll.draw_controller()
		
		
		#視覚用
		time.sleep(sleep_time)
		pygame.display.update()# 画面を更新
main()


###プロファイル用
"""
import cProfile
import pstats
from pstats import SortKey
pr = cProfile.Profile()
pr.runcall(main)
stats = pstats.Stats(pr)
stats.sort_stats('cumtime')
stats.print_stats(30)
"""
