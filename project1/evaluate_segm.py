import sys
import argparse
from itertools import izip

def precision(file1, file2):
	file1 = open(file1, 'r')
	all_found = 0
	correct = 0
	file2 = open(file2, 'r')
	for line1, line2 in izip(file1, file2):
		boundaries_1 = [1]
		i = 0
		while i < len(line1): 
			if i == len(line1)-1:
				b = 1
			elif line1[i + 1] == ' ':
				b = 1
			else:
				b = 0
			boundaries_1.append(b)
			i = i + 1
		i = 0
		boundaries_2 = [1]
		while i < len(line2): 
			if i == len(line2)-1:
				b = 1
			elif line2[i + 1] == ' ':
				b = 1
			else:
				b = 0
			boundaries_2.append(b)
			i = i + 1	
		j = 0
		while j < len(boundaries_1):
			if boundaries_1[j] == 1 and boundaries_2[j] == 1:
					i = j + 1
					while i < len(boundaries_1) and boundaries_1[i]== 0 and boundaries_2[i] == 0:
						i = i + 1
					if i < len(boundaries_1):
						if boundaries_2[i] == boundaries_1[i] and boundaries_2[i] == 1:
							correct = correct + 1
							j = i	
						else:
							i = j + 1 
							while i < len(boundaries_1) and boundaries_1[i] == 0:
								i = i + 1
							j = i
					else:
						break
			else:
				j = j + 1
		sp1 = line1.split()
#		sp2 = line2.split()
		all_found = len(sp1) + all_found
 #		i = 0
#		while i < len(sp1):
#			if sp1[i] == sp2[i]:
#				correct = correct + 1
#			i = i + 1
	precision = (correct * 1.0 / all_found * 1.0)*100
	print 'Precision: '+ str(precision)	
	return precision

def recall(file1, file2):
	file1 = open(file1, 'r')
	all_correct = 0
	correct = 0
	file2 = open(file2, 'r')
	for line1, line2 in izip(file1, file2):
		boundaries_1 = [1]
		i = 0
		while i < len(line1): 
			if i == len(line1)-1:
				b = 1
			elif line1[i + 1] == ' ':
				b = 1
			else:
				b = 0
			boundaries_1.append(b)
			i = i + 1
		i = 0
		boundaries_2 = [1]
		while i < len(line2): 
			if i == len(line2)-1:
				b = 1
			elif line2[i + 1] == ' ':
				b = 1
			else:
				b = 0
			boundaries_2.append(b)
			i = i + 1	
		j = 0
		while j < len(boundaries_2):
			if boundaries_2[j] == 1 and boundaries_1[j] == 1:
					i = j + 1
					while i < len(boundaries_2) and boundaries_2[i]== 0 and boundaries_1[i] == 0:
						i = i + 1
					if i < len(boundaries_2):
						if boundaries_1[i] == boundaries_2[i] and boundaries_2[i] == 1:
							correct = correct + 1
							j = i	
						else:
							i = j + 1 
							while i < len(boundaries_2) and boundaries_2[i] == 0:
								i = i + 1
							j = i
					else:
						break
			else:
				j = j + 1
		sp = line2.split()
		all_correct = len(sp) + all_correct
#	for line1, line2 in izip(file1, file2):
#		sp1 = line1.split()
#		sp2 = line2.split()
#		all_correct = len(sp2) + all_correct
#		i = 0
#		while i < len(sp1):
#			if sp1[i] == sp2[i]:
#				correct = correct + 1
#			i = i + 1
	recall = (correct * 1.0 / all_correct * 1.0)*100
	print 'Recall: '+  str(recall)
	return recall
	
def f_score(precision, recall):
	f = (2 * precision * recall * 1.0/ (precision + recall)*1.0 )
	print 'F-score: ' + str(f)
	
def main():
    commandline_parser = argparse.ArgumentParser()   
    commandline_parser.add_argument("--input-file", nargs =1, help="Specify the path of the segmented file to evaluate")
    commandline_parser.add_argument("--evaluation-file", nargs =1, help="Specify the path of the correctly segmented file")  
    args = vars(commandline_parser.parse_args())
    input_file = args["input_file"][0]
    eval_file = args["evaluation_file"][0]
    p = precision(input_file, eval_file)
    r= recall(input_file, eval_file)
    f_score(p, r)
    
if __name__ == '__main__':
	main()
	 