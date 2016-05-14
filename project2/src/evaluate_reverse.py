import os
import Story
from Get_Input_Reverse import read_corpus_file, process_corpus
from collections import defaultdict
from random import shuffle

#Values to collect for the evaluation
values = {'all_correct_seq': 0,'correct_seq':0,'all_correct_words':0,
			'all_found_words': 0, 'correct_words': 0, 'found_words':0, 'error_words':0, 'error_seq': 0,
			'error_length':0, 'error_too_short':0, 'error_too_long':0, 'error_order_words':0, 
			'error_order_sequences':0, 'error_new_word':0}
for v in values.keys():
	values[v] = defaultdict(int)

#Collect values for a task (going through all the stories)
def values_task(test, output):
	for story_test, story_output in zip(test, output):
		story_test = story_test.raw_texts
		story_output = story_output.raw_texts
		for x,y in zip(story_test, story_output):
			#x = reverse(x)
			x = x[::-1]
			#Same sequence: correct!
			if x == y:
				values['correct_seq'][len(x)] += 1
			else:
			#Wrong sequence
				values['error_seq'][len(x)]+= 1
			values['all_correct_seq'][len(x)] += 1
			#Wron length
			if len(x) != len(y):
				values['error_length'][len(x)] += 1
				if len(x) < len(y): 
					values['error_too_long'][len(x)] += 1
				else:
					values['error_too_short'][len(x)] += 1
			i = 0
			j = 0
			values['all_correct_words'][len(x)] += len(x)
			values['all_found_words'][len(x)] += len(y)
			#Values for word accuracy			
			while i < len(y):
				if y[i] == x[i]:
					values['correct_words'][len(x)] += 1
				elif y[i] in x:
					#Error in word order
					values['error_words'][len(x)] += 1
					values['error_order_words'][len(x)] += 1
					j += 1
				else:
					 # A word that is not in y is in x
					values['error_words'][len(x)] += 1
					values['error_new_word'][len(x)] += 1
				i += 1
			if j == len(x) and j == len(y):
				# Right words but wrong order
				values['error_order_sequences'][len(x)] += 1

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
		print ('\t Sequence length '+ str(x) + ': ' + str(accuracy_seq[x]))
	print ('Precision of words: ')
	for x in precision_words.keys():
		print ('\t Sequence length '+ str(x) + ': ' + str(precision_words[x]))
	print ('Recall of words: ')
	for x in recall_words.keys():
		print ('\t Sequence length '+ str(x) + ': ' + str(recall_words[x]))
	print ('F1 score of words: ')
	for x in f_words.keys():
		print ('\t Sequence length '+ str(x) + ': ' + str(f_words[x]))
	print ('Percentage of errors for different length: \n')
	for x in error_length.keys():
		print ('\t Sequence length '+ str(x) + ': ' + str(error_length[x]))
	print ('Percentage of errors for longer length: ')
	for x in error_too_long.keys():
		print ('\t Sequence length '+ str(x) + ': ' + str(error_too_long[x]))
	print ('Percentage of errors for shorter length: ')
	for x in error_too_short.keys():
		print ('\t Sequence length '+ str(x) + ': ' + str(error_too_short[x]))
	print ('Percentage of errors for word order (same length): ')
	for x in error_word_order.keys():
		print ('\t Sequence length '+ str(x) + ': ' + str(error_word_order[x]))
	print ('Percentage of errors for a new word: ')
	for x in error_new_word.keys():
		print ('\t Sequence length '+ str(x) + ': ' + str(error_new_word[x]))
	
if __name__ == '__main__':
	reverse_folder = '../data/data_answer/test'
	output_folder = '../data/data_answer/test'
	# Going through all the tasks in the test set
	for f in os.listdir(reverse_folder)[:5]:
		fn_test = os.path.join(reverse_folder, f)
		#fn_output = os.path.join(output_folder, f)
		#fn_output = os.path.join(output_folder, f)
		#fn_output = open(fn_output, 'r')
		# Collect stories for a task
		test_stories = list(process_corpus(fn_test))
		fn_output = test_stories
		values_task(test_stories, fn_output)
	evaluate()