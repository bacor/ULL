import sys
import argparse
from itertools import izip

#Compute precision
def precision(correct, all_found, s):
	p = (correct * 1.0 / all_found * 1.0)*100
	print "Precision of " + s+ ': '+ str(p)
	return p

#Compute recall
def recall(correct, all_correct, s):
	r = (correct * 1.0 / all_correct * 1.0)*100
	print "Recall of " + s + ': '+ str(r)
	return r
	
#Compute fscore
def f_score(precision, recall,s):
	f = (2 * precision * recall * 1.0/ (precision + recall)*1.0 )
	print 'F-score of ' + s  + ': '+ str(f) 

#Compute precision, recall, fscore for words (both word boundaries must be correctly identified to count as correct)
def eval_words(file1, file2):
	file1 = open(file1, 'r')
	all_found = 0
	all_correct = 0
	correct = 0
	file2 = open(file2, 'r')
	#Analysis of both file line by line
	for line1, line2 in izip(file1, file2):
		#The lines are turned into a list representation where each charachter is assigned to 1 when it is followed by a word boundaries (i.e. space), 0 otherwise
		#the lists has a boundaries at the beginning (start boundary of the first word)
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
		#Check whether both boundaries are respected 		
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
		sp2 = line2.split()
		#All correct: all words in golden set
		all_correct = len(sp2) + all_correct
		#All found: all words in input file
		all_found = len(sp1) + all_found
	s = 'words'
	p = precision(correct, all_found,s)
	r = recall(correct, all_correct,s)
	f_score(p, r, s)

#Compute precision, recall, fscore for word types 
def eval_lexicon(file1, file2):
	file1 = open(file1, 'r')
	#Build lexicon of both the files
	lexicon1 = []
	for line in file1:
		sp = line.split()
		for w in sp:
			if w not in lexicon1:
				lexicon1.append(w)
	lexicon2 = []
	file2 = open(file2, 'r')
	for line in file2:
		sp = line.split()
		for w in sp:
			if w not in lexicon2:
				lexicon2.append(w)
	correct = 0
	found = len(lexicon1)
	for w in lexicon1:
		if w in lexicon2:
			#Correct if a word in lexicon1 is in lexicon2
			correct = correct + 1
	s = 'lexicon'	
	#All found: words in the list of lexicon1
	all_found = len(lexicon1)
	p = precision(correct, all_found, s)
	#All correct: words in the list of lexicon2
	all_correct = len(lexicon2)
	r = recall(correct, all_correct, s)
	f_score(p, r,s)

#Compute precision, recall, fscore for potentially ambiguous boundaries (boundaries without utterance boundaries)
def eval_boundaries(file1, file2):
	file1 = open(file1, 'r')
	file2 = open(file2, 'r')
	correct = 0
	all_found = 0
	all_correct = 0
	#Analysis of files line by line
	for line1, line2 in izip(file1, file2):
		#The lines are turned into a list such that each charachter is assigned 1 if it is followed by a word boundary, 0 otherwise
		boundaries_1 = []
		i = 0
		while i < len(line1): 
			if i == len(line1)-1: 
				#Utterance boundaries do not count as boundaries
				b = 0
			elif line1[i + 1] == ' ':
				b = 1
				#All found: number of boundaries in file1 without utterance boundaries
				all_found = all_found + 1
			else:
				b = 0
			boundaries_1.append(b)
			i = i + 1
		i = 0
		boundaries_2 = []
		while i < len(line2): 
			if i == len(line2)-1:
				b = 0
			elif line2[i + 1] == ' ':
				b = 1
				#All correct: number of boundaries in file2 without utterance boundaries
				all_correct = all_correct + 1
			else:
				b = 0
			boundaries_2.append(b)
			i = i + 1
		j = 0
		while j < len(boundaries_1):
			if boundaries_1[j] == 1 and boundaries_1[j] == 1:
				#Correct if a boundary is set in the two lines in the same place
				correct = correct + 1
			j = j + 1
	s = 'boundaries'
	p = precision(correct, all_found, s)
	r = recall(correct, all_correct, s)
	f_score(p, r,s)
		
def main():
    commandline_parser = argparse.ArgumentParser()  
    # Argument: input file = file to evaluate ()segmented test set)
    commandline_parser.add_argument("--input-file", nargs =1, help="Specify the path of the segmented file to evaluate")
    # Argument: evaluation file = golden segmented test set
    commandline_parser.add_argument("--evaluation-file", nargs =1, help="Specify the path of the correctly segmented file")  
    args = vars(commandline_parser.parse_args())
    input_file = args["input_file"][0]
    eval_file = args["evaluation_file"][0]
   # Precision, Recall, Fscore for words
    eval_words(input_file, eval_file)
	#Precision, Recall, Fscore for the lexicon (word types)
    eval_lexicon(input_file, eval_file)
    # Precision, Recall, Fscore for potentially ambiguous boundaries (utterance boundaries not included)
    eval_boundaries(input_file, eval_file)
    
if __name__ == '__main__':
	main()
	 