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
		with open("memory.json","r") as f:
			m = json.loads(str(f.read()))
		return m
	return {}

def mem_dump(memory):
	with open("memory.json","w+") as f:
		f.write(json.dumps(memory))

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

def question(memory):
	user = choice(memory.keys())
	if getrandbits(1):
		general = choice(list(set([str(i) for j in [memory[x][0].keys() for x in memory] for i in j])))
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

if __name__ == "__main__":
	memory = mem_load()
#	memory = mem_ins(memory,inp())
	question(memory)
	mem_out(memory)
	mem_dump(memory)
