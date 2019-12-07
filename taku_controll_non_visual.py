


def main():
	import taku
	import sys
	import time
 
	
	#init
	#卓の設定
	numOfPeople=2
	numOfAkadora=1
	numOfSet=2
	print_b=True
	
	#import prototype
	#agent=prototype.agent()
	taku=taku.taku(numOfPeople,numOfAkadora,numOfTonpu=1,numOfSet=numOfSet,torikiri=True,saifu=True)
	# ゲームループ
	while True:

		if print_b and taku.state=='kyoku_start':
			print('%s kyoku,%s honba,%s'%(taku.kyoku,taku.honba,taku.tokuten.tokuten))
		taku.controll()
		if taku.state=='finished':
			print('')
			print('finished')
			print('%s kyoku,%s honba,%s'%(taku.kyoku,taku.honba,taku.tokuten.tokuten))
			break
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
