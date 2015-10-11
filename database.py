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

def mem_load(a):
	try:
		if path.isfile("memory.json"):
			with open("memory.json","r+") as f:
				m = json.loads(str(f.read()))
			return m[a]
	except ValueError:
		pass
	return {}

def all_load():
	with open("memory.json","r+") as f:
		m = json.loads(str(f.read()))
	return m

def mem_dump(memory,name):
	with open("memory.json","w+") as f:
		all = all_load()
		all[name] = memory
		json.dump(all, f)

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
