import os
import Story
from Get_Input_Reverse import read_corpus_file, process_corpus
from collections import defaultdict
import random

#Values to collect for the evaluation
values = {'all_correct_len': 0,'correct_len':0,'all_correct_facts': 0,'correct_facts':0, 'all_correct_task': 0, 'correct_task':0, 
			'error_wordinstory_len': 0, 'error_len': 0, 'error_wordinstory_facts': 0, 'error_facts': 0, 'error_wordinstory_task': 0, 'error_task': 0}
for v in values.keys():
	values[v] = defaultdict(int)

#Collect values for a task (going through all the stories)
def values_task(test, output, id_task):
	answers_test = []
	
	#CHANGE!!!
	answers_output = []
	#for line in output:
	#	answers_output.append(line.strip('\n'))
	i = 0
	for story_test in test:
		answers = list(story_test.answers)
		
		#if answers == []:
		#	print (story_test.raw_texts[len(story_test.raw_texts)-1], id_task)
		len_story = len(story_test.raw_texts) - len(story_test.questions)
		values['all_correct_len'][len_story] += len(answers)
		values['all_correct_task'][id_task] += len(answers)		
		for a in answers:
			answers_test.append(a[0])
			facts = len(a[1])
			values['all_correct_facts'][facts] += 1
			#if i == 0:
			#	a_output = random.choice(random.choice(list(story_test.raw_texts)))
			#else:			
			a_output = random.choice(random.choice(list(test[random.choice(range(len(test)))].raw_texts)))
			#a_output = a[0]		
			answers_output.append(a_output)
			if a[0] == a_output:
				values['correct_len'][len_story] += 1
				values['correct_task'][id_task] += 1
				values['correct_facts'][facts] += 1
			else:
				values['error_len'][len_story] += 1
				values['error_task'][id_task] += 1
				values['error_facts'][facts] += 1
				for line in story_test.raw_texts:
					if a_output in line:
						values['error_wordinstory_len'][len_story] += 1
						values['error_wordinstory_task'][id_task] += 1
						values['error_wordinstory_facts'][facts] += 1
						break
		i += 1
		
#Computing the final evaluation using the values collected
def evaluate():
	#Accuracy of the sequences
	accuracy_len= {}
	accuracy_task= {}
	accuracy_facts = {}
	error_wordinstory_len = {}
	error_wordinstory_task = {}
	error_wordinstory_facts = {}
	# Compute value for sequences of each length
	for i in values['all_correct_len'].keys():
		accuracy_len[i] = (values['correct_len'][i]*1.0)/(values['all_correct_len'][i]*1.0)
	for i in values['all_correct_task'].keys():	
		accuracy_task[i] = (values['correct_task'][i]*1.0)/(values['all_correct_task'][i]*1.0) 
	for i in values['all_correct_facts'].keys():	
		accuracy_facts[i] = (values['correct_facts'][i]*1.0)/(values['all_correct_facts'][i]*1.0) 
	for i in values['error_wordinstory_len'].keys():	
		if values['error_len'][i] != 0:
			error_wordinstory_len[i] = (values['error_wordinstory_len'][i]*1.0)/(values['error_len'][i]*1.0) *100
	for i in values['error_wordinstory_task'].keys():		
		if values['error_task'][i] != 0:
			error_wordinstory_task[i] = (values['error_wordinstory_task'][i]*1.0)/(values['error_task'][i]*1.0) *100
	for i in values['error_wordinstory_facts'].keys():	
		if values['error_facts'][i] != 0:
			error_wordinstory_facts[i] = (values['error_wordinstory_facts'][i]*1.0)/(values['error_facts'][i]*1.0) *100
			
	# Compute value for sequences of any length
	accuracy_len['All'] = (sum(values['correct_len'].values())*1.0)/(sum(values['all_correct_len'].values())*1.0) 
	accuracy_task['All'] = (sum(values['correct_task'].values())*1.0)/(sum(values['all_correct_task'].values())*1.0) 
	if sum(values['error_len'].values()) != 0:
		error_wordinstory_len['All']= (sum(values['error_wordinstory_len'].values())*1.0)/(sum(values['error_len'].values())*1.0) *100
		error_wordinstory_task['All']= (sum(values['error_wordinstory_task'].values())*1.0)/(sum(values['error_task'].values())*1.0) *100
		
	print ('Accuracy of answers: ')
	for x in accuracy_len.keys():
		if x == 'All':
			print ('\t Story length '+ str(x) + ' ('+ str(sum(values['all_correct_len'].values())) + '): ' + str(accuracy_len[x]))
		else:
			print ('\t Story length '+ str(x) + ' ('+ str( values['all_correct_len'][x]) + '): ' + str(accuracy_len[x]))
	for x in accuracy_task.keys():
		if x == 'All':
			print ('\t Task '+ str(x) + ' ('+ str(sum(values['all_correct_task'].values())) + '): ' + str(accuracy_task[x]))
		else:
			print ('\t Task '+ str(x) + ' ('+ str(values['all_correct_task'][x]) + '): '  + str(accuracy_task[x]))
	for x in accuracy_facts.keys():
		if x == 'All':
			print ('\t Supporting facts '+ str(x) + ' ('+str(sum(values['all_correct_facts'].values())) + '): ' + str(accuracy_facts[x]))
		else:
			print ('\t Supporting facts '+ str(x) + ' ('+str(values['all_correct_facts'][x]) + '): ' + str(accuracy_facts[x]))
	print ('Percentage of wrong answers with words in the stories: ')
	for x in error_wordinstory_len.keys():
		if x == 'All':
			print ('\t Story length '+ str(x) + ' ('+str( sum(values['all_correct_len'].values())) + '): ' + str(error_wordinstory_len[x]))
		else:
			print ('\t Story length '+ str(x) + ' ('+str( values['all_correct_len'][x]) + '): ' + str(error_wordinstory_len[x]))
	for x in error_wordinstory_task.keys():
		if x == 'All':
			print ('\t Task '+ str(x) + ' ('+str(sum(values['all_correct_task'].values())) + '): '+ str(error_wordinstory_task[x]))
		else:
			print ('\t Task '+ str(x) + ' ('+str(values['all_correct_task'][x]) + '): '+ str(error_wordinstory_task[x]))
	for x in error_wordinstory_facts.keys():
		if x == 'All':
			print ('\t Supporting facts '+ str(x) + ' ('+str(x) + str(sum(values['all_correct_facts'].values()))+ '): ' + str(error_wordinstory_facts[x]))
		else:
			print ('\t Supporting facts '+str(x) + ' ('+ str(x) + str(values['all_correct_facts'][x]) + '): ' + str(error_wordinstory_facts[x]))

	
if __name__ == '__main__':
	answer_folder = '../data/data_answer/test'
	output_folder = '../data/data_answer/test'
	# Going through all the tasks in the test set
	for f in sorted(os.listdir(answer_folder)):
		fn_test = os.path.join(answer_folder, f)
		fn_output = os.path.join(output_folder, f)
		fn_output = open(fn_output, 'r')
		# Collect stories for a task
		test_stories = list(process_corpus(fn_test))
		fn_output = test_stories
		values_task(test_stories, fn_output, f)
	evaluate()
