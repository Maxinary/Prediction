#!/usr/bin/python
import re
import json
from os import path
from random import getrandbits, choice
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

def mem_load():
	if path.isfile("memory.json"):
		with open("memory.json","r+") as f:
			m = json.loads(str(f.read()))
		return m
	return {}

def mem_dump(memory):
	with open("memory.json","w+") as f:
		json.dump(memory, f)

def mem_out(memory):
	x = str(raw_input(".au do ma\n>"))
	if x in memory.keys():
		for i in memory[x][0]:
			print x+" .ao "+i+" "+memory[x][0][i]
		for i in [l for l in memory[x][1]]:
				print x+" "+i
	else:
		print "mi na sispe'i ta"

def dict_ins(memory,value):
	name = value[0]
	key = value[1].keys()[0]
	vale = value[1][key]
	if value[0] in memory.keys():
		memory[value[0]][0][value[1].keys()[0]] = value[1][value[1].keys()[0]]						
	else:
		memory[value[0]] = [{value[1].keys},[],[]]
	return memory

def true_ins(memory,value):
	if value[0] in memory.keys():
		if value[1] not in memory[value[0]][1]:
			memory[value[0]][1].append(value[1])
		if value[1] in memory[value[0]][2]:
			memory[value[0]][2].remove(value[1])
	else:
		memory[value[0]] = [{},[value[1]],[]]
	return memory

def false_ins(memory,value):
	if value[0] in memory.keys():
		if value[1] not in memory[value[0]][2]:
			memory[value[0]][2].append(value[1])
		if value[1] in memory[value[0]][1]:
			memory[value[0]][1].remove(value[1])
	else:
		memory[value[0]] = [{},[],[value[1]]]
	return memory

def mem_ins(memory,value):
	if str(value[1].__class__) == "<type 'dict'>":
		memory = dict_ins(memory,value)
	elif value[2]:
		memory = true_ins(memory,(value[0],value[1]))
	else:
		memory = false_ins(memory,(value[0],value[1]))
	return memory

def question_smart(memory):#todo sum chance of probabilities
	fin = ("",0)
	general = match(memory)
	users = memory.keys()
	
	for x in memory.keys():
		u_dat = {x:("",0) for x in memory.keys()}
	for user in users:
		u_attrs = [str(x) for x in memory[user][1]]+[str(x) for x in memory[user][2]]
		for i in memory[user][1]:
			for j in general[i]:
				if general[i][j][0]+general[i][j][1]!=0:
					value = general[i][j][0]
					value /= float(general[i][j][1]+general[i][j][0])
					value -= 0.5#minimum -.5, maximum +.5
					if j not in u_attrs and abs(value)>abs(u_dat[user][1]):#doesn't ask about traits already used
						u_dat[user] = (j,value)
	print u_dat
	fin = ("",0)
	for u in users:
		if abs(u_dat[u][1]) > fin[1]:
			print u
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
		

def question_rand(memory):
	user = choice(memory.keys())
	if getrandbits(1):
		general = list(set([str(i) for j in [memory[x][0].keys() for x in memory] for i in j]))
		for i in memory[user][0]:
			general.remove(i)
		general = choice(general)
		vale = raw_input(
			user+
			" .ao "+
			general+
			" ma\n>"
		)
		dict_ins(memory,(user,{general:vale}))
	else:
		attr = choice(list(set([str(i) for j in [memory[x][1]+memory[x][2] for x in memory] for i in j])))

		vale = raw_input(
			"xu "+
			user+
			" "+
			attr+
			"\n>"
		)
		if vale == "go'i":
			true_ins(memory,(user,attr))
		elif vale == "nelci":
			false_ins(memory,(user,attr))

def match(memory):
	#All points where x and y are correlated
	#if x has y in it:
	#	if x.y is true:score+=1
	#	else score-=1
	all = list(set([str(i) for j in [memory[x][1]+memory[x][2] for x in memory] for i in j]))
	f_count = {}
	for i in all:
		f_count[i] = {}
		for j in all:
			if j!=i:
				f_count[i][j] = [0,0]#[amount who have correlation(both true), amount who have opposite value (x is true, y is false)]
	t = [memory[i][1] for i in memory.keys()]
	f = [memory[i][2] for i in memory.keys()]
	u_all = [memory.keys()]
	for i in t:
		for j in i:
			for k in i:
				if k!=j:
					f_count[k][j][0]+=1
	for i in range(len(t)):
		for j in t[i]:
			for k in f[i]:
				if j!=k:
					f_count[j][k][1]+=1
					f_count[k][j][1]+=1
	return f_count

if __name__ == "__main__":
	memory = mem_load()
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
					print i,":",memory[i],"\n"
			elif inpu == "match":
				x = match(memory)
				for i in x:
					print i,":",x[i],"\n"
	print memory
	print
	print match(memory)
	mem_dump(memory)
