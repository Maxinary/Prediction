#!/usr/bin/python
import re
import json
from os import path
from random import getrandbits, choice
from database import *
''' 
The way it works:
	it stores as {noun:[{general_attributes:value,,,},[True,Values],[False,Values]]}

'''

def inp():
	x = str(raw_input("ko talva mi\n>"))
	if re.match("^\w+ \w+$", x):
		noun = x[:x.find(" ")]
		adjective = x[x.find(" ")+1:]
		return (noun,adjective,True)
	elif re.match("^\w+ na \w+$",x):
		words = x.split(" ")
		noun = words[0]
		adjective = words[2]
		return (noun,adjective,False)
	elif re.match("\w+ \.ao \w+ \w+",x):#implemented .ao as attribute x2 'of' x1 is x3
		words = x.split(" ")
		del words[1]
		return (words[0],{words[1]:words[2]})

def question_smart(memory):#todo sum chance of probabilities
			   #uber frequentism
	fin = ("",0)
	general = frequentist_match(memory)
	users = memory.keys()
	
	for x in memory.keys():
		u_dat = {x:("",0) for x in memory.keys()}
	for user in users:
		u_attrs = [str(x) for x in memory[user][1]]+[str(x) for x in memory[user][2]]
		for i in memory[user][1]:
			for j in general[i]:
				value = general[i][j]
				if j not in u_attrs and abs(value)>abs(u_dat[user][1]):#doesn't ask about traits already used
					u_dat[user] = (j,value)
	fin = ("",0)
	for u in users:
		if abs(u_dat[u][1]) > abs(fin[1]):
			user = u
			fin = (u_dat[u][0],u_dat[u][1])

	if fin == ("",0):
		print "Fully explored"
		return
	attr = fin[0]
	if fin[1]<=0:
		inter = " na "
	else:
		inter = " "
	vale = raw_input(
		"xu "+
		user+
		inter+
		attr+
		"\n>"
	)
	if fin[1]>0:
		if vale == "go'i":
			true_ins(memory,(user,attr))
		elif vale == "nelci":
			false_ins(memory,(user,attr))
	else:
		if vale == "nelci":
			true_ins(memory,(user,attr))
		elif vale == "go'i":
			false_ins(memory,(user,attr))
		
def frequentist_match(memory):
	#All points where x and y are correlated
	#if x has y in it:
	#	if x.y is true:score+=1
	#	else score-=1
	all = list(set([str(i) for j in [memory[x][1]+memory[x][2] for x in memory] for i in j]))
	f_count = {}
	t_abs = {}
	for i in all:
		t_abs[i] = 0
		f_count[i] = {}
		for j in all:
			if j!=i:
				f_count[i][j] = [0,0]#[amount who have correlation(both true), amount who have opposite value (x is true, y is false)]
	t = [memory[i][1] for i in memory.keys()]
	f = [memory[i][2] for i in memory.keys()]
	u_all = [memory.keys()]
	for i in t:
		for j in i:
			t_abs[j]+=1
			for k in i:
				if k!=j:
					f_count[k][j][0]+=1
	for i in range(len(t)):
		for j in t[i]:
			for k in f[i]:
				if j!=k:
					f_count[j][k][1]+=1
					f_count[k][j][1]+=1
	#turn into percentage odds
	for i in f_count:
		for j in f_count[i]:
			sum = f_count[i][j][0]+f_count[i][j][1]
			if f_count[i][j][0]+f_count[i][j][1]!=0:
				f_count[i][j] = float(f_count[i][j][0])/(f_count[i][j][1]+f_count[i][j][0])
			else:
				f_count[i][j] = .5
			#multiply by the percent of population who have the attribute(or for negative, don't have the attribute)
			f_count[i][j]-=.5
			f_count[i][j]*=200
	return f_count


if __name__ == "__main__":
	memory = mem_load("noun")
	inpu = ""
	while inpu!="exit":
		inpu = raw_input("~ ")
		if re.match("^\d+",inpu):
			num = re.findall("^\d+",inpu)[0]
			c = int(num)
			inpu = inpu[len(num):]
			print inpu
		else:
			c = 1
		for i in range(0,c):
			if inpu == "setca":
				me = inp()
				if me is not None:
					memory = mem_ins(memory,me)
			elif inpu == "retsku":
				question_smart(memory)
			elif inpu == "help":
				print "setca:insert info"
				print "retsku: question me"
				print "memory: dump all memory"
				print "match: show current matching data"
				print "exit:exit"
			elif inpu == "memory":
				for i in memory:
					print "\n",i,":"
					for j in i:
						print "	",j,":",memory[i][j]
			elif inpu == "match":
				x = frequentist_match(memory)
				for i in x:
					print "\n",i,":"
					for j in x[i]:
						print "	",j,":",x[i][j]
	mem_dump(memory,"noun")
