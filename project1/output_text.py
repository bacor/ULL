from helpers import *
import ast
import os 

file_name = "data" + os.path.sep + "br-phono-train.txt"

corpus = read_data(file_name)
c, U = clean_corpus( "$".join(corpus) )
boundary_content = open("results/dp_bigram_.txt","r").read()
boundaries = eval(boundary_content[boundary_content.index(":>")+2:])
text = ''
i = 0
corpus = ''.join(line for line in corpus)
for c, b in zip(corpus, boundaries):
	if i == 0:
		char = c
	elif b == 1 and i not in U:
		char = ' '+ c
	elif 	b == 1 and i in U:
		char = '\n' + c
	else:
		char = c
	text = text + char
	i = i + 1
output_text = open("results/dp_bigram.txt","w")
output_text.write(text)
output_text.close()