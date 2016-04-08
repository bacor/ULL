import sys
import argparse
from itertools import izip

def precision(file1, file2):
	file1 = open(file1, 'r')
	all_found = 0
	correct = 0
	file2 = open(file2, 'r')
	for line1, line2 in izip(file1, file2):
		sp1 = line1.split()
		sp2 = line2.split()
		all_found = len(sp1) + all_found
		i = 0
		while i < len(sp1):
			if sp1[i] == sp2[i]:
				correct = correct + 1
			i = i + 1
	precision = (correct * 1.0 / all_found * 1.0)*100
	print 'Precision: '+ str(precision)	
	return precision

def recall(file1, file2):
	file1 = open(file1, 'r')
	all_correct = 0
	correct = 0
	file2 = open(file2, 'r')
	for line1, line2 in izip(file1, file2):
		sp1 = line1.split()
		sp2 = line2.split()
		all_correct = len(sp2) + all_correct
		i = 0
		while i < len(sp1):
			if sp1[i] == sp2[i]:
				correct = correct + 1
			i = i + 1
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
	 