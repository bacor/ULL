import os
import Story
from Get_Input_Reverse import read_corpus_file, process_corpus
from collections import defaultdict
import random

#Values to collect for the evaluation
values = {'all_correct_seq': 0,'correct_seq':0,'all_correct_words':0,
		'all_found_words': 0, 'correct_words': 0, 'found_words':0, 'error_words':0, 'error_seq': 0,
		'error_length':0, 'error_too_short':0, 'error_too_long':0, 'error_order_words':0, 
		'error_order_sequences':0, 'error_new_word':0}
for v in values.keys():
	values[v] = defaultdict(int)
ac_seq_file = open('accuracy_sequences.txt', 'w')

#Collect values for a task (going through all the stories)
def values_task(dataset, output):
	vocab = set()
	#for story_test, story_output in zip(test, output):
	#	story_test = story_test.raw_texts
		#story_output = story_output.raw_texts
		#for y,x in zip(story_test, story_output):
	#	for x in story_test:
	for line_dataset, line_output in zip(dataset, output):
		line_dataset = line_dataset.split()
		line_output = line_output.split()
		for i in line_dataset:
			vocab.add(i)
		i = 0
		y = []
		while i < random.choice(range(2,10)):
			line_output.append(random.choice(list(vocab)))
			i += 1
		#Same sequence: correct!
		if line_dataset == line_output:
			values['correct_seq'][len(line_dataset)] += 1
		else:
		#Wrong sequence
			values['error_seq'][len(line_dataset)]+= 1
		values['all_correct_seq'][len(line_dataset)] += 1
		#Wron length
		if len(line_dataset) != len(line_output):
			values['error_length'][len(line_dataset)] += 1
			if len(line_dataset) < len(line_output): 
				values['error_too_long'][len(line_dataset)] += 1
			else:
				values['error_too_short'][len(line_dataset)] += 1
		i = 0
		j = 0
		values['all_correct_words'][len(line_dataset)] += len(line_dataset)
		values['all_found_words'][len(line_dataset)] += len(line_output)
		#Values for word accuracy
		correct = 0
		while i < len(line_output):
			if i < len(line_dataset):
				if line_dataset[i] == line_output[i]:
					values['correct_words'][len(line_dataset)] += 1
					correct += 1
				elif line_output[i] in line_dataset:
					#Error in word order
					values['error_words'][len(line_dataset)] += 1
					values['error_order_words'][len(line_dataset)] += 1
					j += 1
				else:
				 # A word that is not in y is in x
					values['error_words'][len(line_dataset)] += 1
					values['error_new_word'][len(line_dataset)] += 1
			else:
				values['error_words'][len(line_dataset)] += 1
				if line_output[i] in line_dataset:
					#Error in word order
					values['error_order_words'][len(line_dataset)] += 1
				else:
				 # A word that is not in y is in x
					values['error_new_word'][len(line_dataset)] += 1
			i += 1
			precision = correct*1.0/len(line_dataset)*1.0
			recall = correct*1.0/len(line_output)*1.0
			if precision + recall != 0:
				f_score = 2 * precision *recall/(precision + recall)*1.0
			else:
				f_score = 0
			ac_seq_file.write(str(correct) + '\t' + str(len(line_dataset)) + '\t' + str(precision) + '\t'  + str(recall) + '\t' + str(f_score) + '\n')
		if j == len(line_output) and j == len(line_dataset):
			# Right words but wrong order
			values['error_order_sequences'][len(len_dataset)] += 1

#Computing the final evaluation using the values collected
def evaluate():
	#Accuracy of the sequences
	accuracy_seq = {}
	#Accuracy of the words in the sequences
	precision_words = {}
	recall_words = {}
	f_words = {}
	#Percentages about errors given by wrong length
	error_too_short = {}
	error_too_long = {}
	error_length = {}
	#Percentages about errors given by word order 
	error_word_order = {}
	error_order_sequence = {}
	#Percentage about errors given by a word not in y
	error_new_word = {}
	# Compute value for sequences of each length
	for i in values['all_correct_seq'].keys():
		accuracy_seq[i] = (values['correct_seq'][i]*1.0)/(values['all_correct_seq'][i]*1.0) 
		precision_words[i] = (values['correct_words'][i]*1.0)/(values['all_correct_words'][i]*1.0) 	
		recall_words[i] = (values['correct_words'][i]*1.0)/(values['all_found_words'][i]*1.0)
		if (precision_words[i])+(recall_words[i]) != 0:
			f_words[i] = 2 * ((precision_words[i])*(recall_words[i]) *1.0)/((precision_words[i])+(recall_words[i])*1.0)
		if values['error_seq'][i] != 0:
			error_length[i] = (values['error_length'][i]*1.0)/(values['error_seq'][i]*1.0) *100
			error_too_long[i] = (values['error_too_long'][i]*1.0)/(values['error_seq'][i]*1.0) *100
			error_too_short[i]= (values['error_too_short'][i]*1.0)/(values['error_seq'][i]*1.0) *100
		if values['error_words'][i] != 0:
			error_word_order[i] = (values['error_order_words'][i]*1.0)/(values['error_words'][i]*1.0) *100
			error_new_word[i] = (values['error_new_word'][i]*1.0)/(values['error_words'][i]*1.0) *100
			
	# Compute value for sequences of any length
	accuracy_seq['All'] = (sum(values['correct_seq'].values())*1.0)/(sum(values['all_correct_seq'].values())*1.0) 
	precision_words['All'] = (sum(values['correct_words'].values())*1.0)/(sum(values['all_correct_words'].values())*1.0) 	
	recall_words['All'] = (sum(values['correct_words'].values())*1.0)/(sum(values['all_found_words'].values())*1.0)
	if (precision_words['All'])+(recall_words['All']) != 0:
		f_words['All'] = 2 * ((precision_words['All'])*(recall_words['All']) *1.0)/((precision_words['All'])+(recall_words['All'])*1.0)
	if sum(values['error_seq']) != 0:
		error_length['All']= (sum(values['error_length'].values())*1.0)/(sum(values['error_seq'].values())*1.0) *100
		error_too_long['All']= (sum(values['error_too_long'].values())*1.0)/(sum(values['error_seq'].values())*1.0) *100
		error_too_short['All'] = (sum(values['error_too_short'].values())*1.0)/(sum(values['error_seq'].values())*1.0) *100	
	if sum(values['error_words'].values()) != 0:
		error_word_order['All']= (sum(values['error_order_words'].values())*1.0)/(sum(values['error_words'].values())*1.0) *100
		error_new_word['All']= (sum(values['error_new_word'].values())*1.0)/(sum(values['error_words'].values())*1.0) *100
				
	print ('Accuracy of sequences: ')
	for x in accuracy_seq.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) + ' (' + str(sum(values['all_correct_seq'].values())) + '): ' + str(accuracy_seq[x]))
		else:
			print ('\t Sequence length '+ str(x) + ' (' + str(values['all_correct_seq'][x]) + '): '  + str(accuracy_seq[x]))
	print ('Precision of words: ')
	for x in precision_words.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) + ' (' + str(sum(values['all_correct_seq'].values())) + '): '+ str(precision_words[x]))
		else:
			print ('\t Sequence length '+ str(x) +  ' (' + str(values['all_correct_seq'][x]) + '): ' + str(precision_words[x]))
	print ('Recall of words: ')
	for x in recall_words.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) +  ' (' + str(sum(values['all_correct_seq'].values())) + '): ' + str(recall_words[x]))
		else:
			print ('\t Sequence length '+ str(x) +  ' (' + str(values['all_correct_seq'][x]) + '): ' + str(recall_words[x]))
	print ('F1 score of words: ')
	for x in f_words.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) +  ' (' + str(sum(values['all_correct_seq'].values())) + '): '+ str(f_words[x]))
		else:
			print ('\t Sequence length '+ str(x) +  ' (' + str(values['all_correct_seq'].values()) + '): ' + str(f_words[x]))
	print ('Percentage of errors for different length: \n')
	for x in error_length.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) +  ' (' + str(sum(values['all_correct_seq'].values())) + '): ' + str(error_length[x]))
		else:
			print ('\t Sequence length '+ str(x) +  ' (' + str(values['all_correct_seq'][x]) + '): ' + str(error_length[x]))
	print ('Percentage of errors for longer length: ')
	for x in error_too_long.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) +  ' (' + str(sum(values['all_correct_seq'].values())) + '): '+ str(error_too_long[x]))
		else:		
			print ('\t Sequence length '+ str(x) +  ' (' + str(values['all_correct_seq'][x]) + '): '+ str(error_too_long[x]))
	print ('Percentage of errors for shorter length: ')
	for x in error_too_short.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) +  ' (' + str(sum(values['all_correct_seq'].values())) + '): ' + str(error_too_short[x]))
		else:
			print ('\t Sequence length '+ str(x) +  ' (' + str(values['all_correct_seq'][x]) + '): ' + str(error_too_short[x]))
	print ('Percentage of errors for word order (same length): ')
	for x in error_word_order.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) + ' (' + str(sum(values['all_correct_seq'].values())) + '): '+ str(error_word_order[x]))
		else:
			print ('\t Sequence length '+ str(x) +  ' (' + str(values['all_correct_seq'][x]) + '): '+ str(error_word_order[x]))
	print ('Percentage of errors for a new word: ')
	for x in error_new_word.keys():
		if x == 'All':
			print ('\t Sequence length '+ str(x) +  ' (' + str(sum(values['all_correct_seq'].values())) + '): ' + str(error_new_word[x]))
		else:
			print ('\t Sequence length '+ str(x) + ' (' + str(values['all_correct_seq'][x]) +'): ' + str(error_new_word[x]))
	
if __name__ == '__main__':
	#reverse_folder = '../data/data_answer/test'
	#output_folder = '../data/data_answer/test'
	# Going through all the tasks in the test set
	#for f in os.listdir(reverse_folder)[:5]:
	dataset = open('../data/data_answer/test/qa1_single-supporting-fact_test.txt', 'r')
	output = open('../data/data_answer/test/qa2_two-supporting-facts_test.txt', 'r')
		#fn_test = os.path.join(reverse_folder, f)
		#fn_output = os.path.join(output_folder, f)
		#fn_output = os.path.join(output_folder, f)
		#fn_output = open(fn_output, 'r')
		# Collect stories for a task
		#test_stories = list(process_corpus(fn_test))
		#fn_output = test_stories
	values_task(dataset, output)
	evaluate()
	ac_seq_file.close()
