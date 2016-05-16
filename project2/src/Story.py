from nltk.tokenize import word_tokenize

class Story:

    def __init__(self, sent_quest_list):        
        self.raw_texts = list(self.get_raw_text(sent_quest_list))
        self.questions = list(self.get_questions(sent_quest_list))
        self.answers = list(self.get_answers(sent_quest_list))

    def get_raw_text(self, sent_quest_list):
        for item in sent_quest_list:
            yield item.text

    def get_questions(self, sent_quest_list):
        for item in sent_quest_list:
            if item.is_question:
                yield item.text
                
    def get_answers(self, sent_quest_list):
        for item in sent_quest_list:
            if item.is_question:
                yield item.answer, [self.raw_texts[i] for i in item.answer_id]

    # initialises the iterator
    # with the current index set to 0
    def __iter__(self):
        self.iterator_state = 0
        self.max_iter = len(self.raw_texts)
        return self

    def __next__(self):
    	if self.iterator_state == self.max_iter:
    		raise StopIteration
    	else:
    		self.iterator_state += 1
    	return self.raw_texts[self.iterator_state-1]
    # returns the next raw text in the story
    # and updates the current index
    # stops iterating when the end of the story is reached
    def next(self):
        if self.iterator_state == self.max_iter:
            raise StopIteration
        else:
            self.iterator_state += 1
            return self.raw_texts[self.iterator_state-1]


class Question:

    def __init__(self, story_id, text, answer, support_fact_id, tokenise=True):
        self.id = story_id
        if tokenise:
            text = word_tokenize(text)
        self.text = text
        self.answer = answer
	#list of supporting facts
        self.answer_id = support_fact_id
        self.is_question = True


class Statement:

    def __init__(self, story_id, text, tokenise=True):
        self.id = story_id
        if tokenise:
            text = word_tokenize(text)
        self.text = text
        self.is_question = False