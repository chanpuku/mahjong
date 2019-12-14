# -*- coding: utf-8 -*-

#メンツの数
#10==9 マンズ
#100==19 マンズ
#200==29 マンズ
#300==37 マンズ
import pickle
import numpy as np
import bisect
import random
S=34#牌の種類
kind=[9,18,27,34]
with open('shanten_data/shanten_key', mode='rb') as fi:
    shanten_key = pickle.load(fi)
with open('shanten_data/shanten_value', mode='rb') as fi:
    shanten_value = pickle.load(fi)

def corrct_id_state_to_id_state(correct_id_state):
	state=correct_id_state
	if len(state)==37:
		ans=np.copy(state[:34])
		ans[4]+=state[34]
		ans[13]+=state[35]
		ans[22]+=state[36]
		return ans


def vectorize_pai_list(pai_list):
    l=[0]*S
    for p in pai_list:
        n=p.id
        l[n]=l[n]+1
    return l
"""
シャンテン数
"""
def Shanten(state,num_of_furoMentsu=0):
	if len(state)==37:state=corrct_id_state_to_id_state(state)
	shanten_k,shanten_t=10,10
	if num_of_furoMentsu==0:
		shanten_t=Shanten_titoi(state)
		shanten_k=Shanten_kokushi(state)
	#対子列挙
	min_s=10
	for i in range(S):
		if state[i]>=2:
			state[i]-=2
			#孤立牌をカット
			p_state = state-kanzen_koritu(state)
			s=Shanten_ippan(p_state,num_of_furoMentsu=num_of_furoMentsu)-1
			min_s=min(s,min_s)
			state[i]+=2
	s= Shanten_ippan(state-kanzen_koritu(state),num_of_furoMentsu=num_of_furoMentsu)
	shanten_i = min(min_s, s)
	return min(shanten_i,shanten_k,shanten_t)



def ukeire(state,num_of_furoMentsu=0):
	if len(state)==37:state=corrct_id_state_to_id_state(state)
	l=[]
	cur=Shanten(state,num_of_furoMentsu=num_of_furoMentsu)
	s=set()
	for i in range(S):
		if i<27:
			if i%9==0:
				if state[i] or state[i+1] or state[i+2]:s.add(i)
			elif i%9==1:
				if state[i-1] or state[i] or state[i+1] or state[i+2]:s.add(i)
			elif i%9==7:
				if state[i-2] or state[i-1] or state[i] or state[i+1] :s.add(i)
			elif i%9==8:
				if state[i-2] or state[i-1] or state[i]:s.add(i)
			else:
				if state[i-2] or state[i-1] or state[i] or state[i+1] or state[i+2]:s.add(i)
		else:
			if state[i]:s.add(i)

	for i in s:
		if state[i]==4:continue
		state[i]+=1
		if Shanten(state,num_of_furoMentsu=num_of_furoMentsu)<cur:
			l.append(i)
		state[i]-=1
	return l

def can_furo_dic(state,num_of_furoMentsu):
	if len(state)==37:state=corrct_id_state_to_id_state(state)
	def can_pon_set(state):
		s=set()
		for i in range(len(state)):
			if state[i]>1:
				s.add(i)
		return s
	def can_daiminkan_set(state):
		s=set()
		for i in range(len(state)):
			if state[i]>2:
				s.add(i)
		return s
	def can_ron_set(state):
		s=set()
		if not Shanten(state,num_of_furoMentsu=num_of_furoMentsu)==0:
			return s
		for i in range(S):
			state[i]+=1
			if Shanten(state,num_of_furoMentsu=num_of_furoMentsu)==-1:
				s.add(i)
			state[i]-=1
		return s
	l={}
	l['pon']=can_pon_set(state)
	l['daiminkan']=can_daiminkan_set(state)
	l['ron']=can_ron_set(state)
	s_chi=set()
	for i in range(9*3):
		if can_chi(state,i):
			s_chi.add(i)
	l['chi']=s_chi
	return l
    
    
def can_chi(state,id):
    if id>26:
        return False
    if id%9==0:
        return state[id+1]*state[id+2]>0
    elif id%9==8:
        return state[id-2]*state[id-1]>0
    elif id%9==1:
        return state[id-1]*state[id+1]>0 or state[id+1]*state[id+2]>0
    elif id%9==7:
        return state[id-2]*state[id-1]>0 or state[id-1]*state[id+1]>0
    else:
        return  state[id-2]*state[id-1]>0 or state[id-1]*state[id+1]>0 or state[id+1]*state[id+2]>0

#chiできる前提
def can_chi_list(correct_id_state,id):
	ans=set()
	state=correct_id_state
	#字牌は考えない
	#retrun はソート順
	if id%9==0:
		if state[id+1]*state[id+2]>0:
			ans.add((id+1,id+2))
	elif id%9==8:
		if state[id-2]*state[id-1]>0:
			ans.add((id-2,id-1))
	elif id%9==1:
		if state[id-1]*state[id+1]>0:
			ans.add((id-1,id+1))
		if state[id+1]*state[id+2]>0:
			ans.add((id+1,id+2))
	elif id%9==7:
		if state[id-2]*state[id-1]>0:
			ans.add((id-2,id-1))
		if state[id-1]*state[id+1]>0:
			ans.add((id-1,id+1))
	else:
		if state[id-2]*state[id-1]>0:
			ans.add((id-2,id-1))
		if state[id-1]*state[id+1]>0:
			ans.add((id-1,id+1))
		if state[id+1]*state[id+2]>0:
			ans.add((id+1,id+2))
	more=set()
	if len(state)==37:
		for a,b in ans:
			if a%9==4 and state[34+(a-4)//9]:more.add((34+(a-4)//9,b))
			if b%9==4 and state[34+(b-4)//9]:more.add((a,34+(b-4)//9))
	return ans|more


        
"""
↓shanten用関数
"""
"""
#完全孤立牌
"""
def koritu_suhai_check(sub_state):
    length = len(sub_state)
    ans = np.zeros(length)
    #i=0
    if sub_state[0] == 1 and 0==sub_state[1] and 0==sub_state[2]:
        ans[0] = 1
    #i=1
    if 0==sub_state[0] and sub_state[1] == 1 and 0==sub_state[2] and 0==sub_state[3]:
        ans[1] = 1
    #i=30==length-3
    for i in range(2, length-2):
        if 0==sub_state[i-2] and 0==sub_state[i-1] and sub_state[i] == 1 and 0==sub_state[i+1] and 0==sub_state[i+2]:
            ans[i] = 1
    j = length-2
    if 0==sub_state[j-2] and 0==sub_state[j-1] and sub_state[j] == 1 and 0==sub_state[j+1]:
        ans[j] = 1
    j = length-1
    if 0==sub_state[j-2] and 0==sub_state[j-1] and sub_state[j] == 1:
        ans[j] = 1
    return ans

#どーせ字牌はチェックしない

def univ(suhai_f,state):
    ans = np.zeros(S)
    ans[0:9]=suhai_f(state[0:9])
    ans[9:18]=suhai_f(state[9:18])
    ans[18:27]=suhai_f(state[18:27])
    return ans

def kanzen_koritu(state):
    return univ(koritu_suhai_check,state)


"""
一般手チェック
"""
def Shanten_ippan(state,num_of_furoMentsu=0):
    #データの場所ーsub_state=長さ９と仮定
    def hash_key(sub_state):
        num=0
        for i in range(9):
            num=num+10**(8-i)*sub_state[i]
        return num
    mA=num_of_furoMentsu#Aのメンツ
    tA=0#Aのターツ
    mB=num_of_furoMentsu#Bのメンツ
    tB=0#Bのターツ
    # 数牌をチェックする処理
    def suhai_check(sub_state,arg):
        mA, tA, mB, tB=arg
        num=hash_key(sub_state)
        if num == 0:
            return mA, tA, mB, tB
        index = bisect.bisect_left(shanten_key,num)
        value=str(shanten_value[index])
        
        for j in range(4-len(value)):
            value = '0'+value
        mA, tA, mB, tB = mA+int(value[2]), tA+int(value[3]), mB+int(value[0]), tB+int(value[1])
        return mA, tA, mB, tB
    #字牌をチェックする処理
    def jihai_check(sub_state,arg):
        mA, tA, mB, tB=arg
        length = len(sub_state)
        for i in range(length):
            if sub_state[i]==2:
                tA,tB=tA+1,tB+1
            elif sub_state[i] > 2:
                mA,mB=mA+1,mB+1
        return mA, tA, mB, tB

    def ippan_univ(suhai_f, jihai_f, state, *arg):
        arg1 = suhai_f(state[0:9], arg)
        arg1 = suhai_f(state[9:18], arg1)
        arg1 = suhai_f(state[18:27], arg1)
        arg1 = jihai_f(state[27:34], arg1)
        return arg1

    mA, tA, mB, tB=ippan_univ(suhai_check, jihai_check, state, mA, tA, mB, tB)
    tA = 4-mA if tA+mA > 4 else tA
    tB = 4-mB if tB+mB > 4 else tB
    
    a=8-2*mA-tA
    b=8-2*mB-tB
    return min(a,b)

"""
チートイチェック
"""
def Shanten_titoi(state,four=False):
    toitsu_suu=0
    syurui_suu=0
    all_shurui_suu=0
    for i in state:
        if i>=1:
            all_shurui_suu=all_shurui_suu+1
            if i>=2:
                toitsu_suu=toitsu_suu+int(i)//2
                syurui_suu=syurui_suu+1

    if four:
        shanten_titoi=6-toitsu_suu
    else:
        all_shurui_suu=7 if all_shurui_suu>7 else all_shurui_suu
        shanten_titoi = 6-syurui_suu+ 7-all_shurui_suu

    return shanten_titoi
"""
国士チェック
"""
def Shanten_kokushi(state):
    shanten_kokushi = 13
    toitsu_suu = 0 #雀頭
    # 19牌をチェックする処理
    def suhai_check(sub_state,arg):
        shanten_kokushi,toitsu_suu=arg
        length = len(sub_state)
        l=[0,length-1]
        for i in l:
            if sub_state[i]:
                shanten_kokushi = shanten_kokushi-1
            if sub_state[i]>=2 and toitsu_suu==0:
                toitsu_suu=1
        return shanten_kokushi,toitsu_suu
    #字牌をチェックする処理
    def jihai_check(sub_state,arg):
        shanten_kokushi, toitsu_suu = arg
        length = len(sub_state)
        for i in range(length):
            if sub_state[i]:
                shanten_kokushi = shanten_kokushi-1
            if sub_state[i]>=2 and toitsu_suu==0:
                toitsu_suu=1
        return shanten_kokushi,toitsu_suu

    def kokushi_univ(suhai_f, jihai_f, state, *shan):
        shan1 = suhai_f(state[0:9], shan)
        shan1 = suhai_f(state[9:18], shan1)
        shan1 = suhai_f(state[18:27], shan1)
        shan1 = jihai_f(state[27:34], shan1)
        return shan1
    shanten_kokushi,toitsu_suu=kokushi_univ(suhai_check, jihai_check, state,shanten_kokushi,toitsu_suu)
    shanten_kokushi = shanten_kokushi-toitsu_suu
    return shanten_kokushi

"""
"""
#####TEST
def state_to_string(state):
	s_l=['m']
	for i in range(S):
		if len(state)==37 and (i==5 or i==14 or i==23):
			if i==5:k=34
			elif i==14:k=35
			else:k=36
			for j in range(state[k]):
					s_l.append('5+')
		if i==9:s_l.append('p')
		elif i==18:s_l.append('s')
		elif i==27:s_l.append('z')
		if state[i]:
			for j in range(state[i]):
				s_l.append(str(i))
	return ''.join(s_l)
def make_state(string):
	state=np.zeros(S)
	sp=0
	for i in range(len(string)):
		if string[i]=='m':
			continue
		elif string[i]=='p':
			sp=9
		elif string[i]=='s':
			sp=18
		elif string[i]=='z':
			sp=27
		elif string[i]=='+':
			state[sp+4]-=1
			state[34+sp//9]+=1
		else:
			state[sp+int(string[i])-1]=state[sp+int(string[i])-1]+1
	return state

"""
#Shanten_ippanに対して全てのsub_stateでTEST
dic={}
l=[set()for i in range(15)]
l[0]={tuple([0]*9)}
for i in range(1,10):
	for j in range(14):
		k=14-j
		for p in range(1,5):
			if k-p<0:break
			for t in l[k-p]:
				li=list(t)
				li[i-1]=p
				l[k].add(tuple(li))

times=0
for i in range(15):
	for t in l[i]:
		mat=np.zeros(34)
		times+=1
		for k in range(9):
			mat[k]=t[k]
		try:
			Shanten_ippan(mat)
		except :
			print(mat)
		if times%3000==2999:print('times =%d'%times)
"""

