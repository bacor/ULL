from Get_Input_Reverse import process_corpus, corpus_to_vecs

import theano
import theano.tensor as T

import numpy as np


class EmbeddingLayer:

    def __init__(self, embedding_init, vocab_size):
        self.embedding_weights = theano.shared(embedding_init(vocab_size))

    def get_outputs(self, inputs):
        embed_vec = lambda row: T.dot(self.embedding_weights, row)
        result, _ = theano.scan(embed_vec, inputs)
        return result

    def get_parameters(self):
        return self.embedding_weights


class RNNLayer:

    def __init__(self, input_weight_init, recurrent_weight_init, bias_init):
        self.input_weights = theano.shared(input_weight_init())
        self.recurrent_weights = theano.shared(recurrent_weight_init())
        self.bias = theano.shared(bias_init())

    def get_outputs(self, input_seq):
        initial_state = T.zeros((self.input_weights.shape[1], ))
        print('initial_state', initial_state.eval())

        hidden_states, updates = theano.scan(fn=self.get_step_outputs,
                                             sequences=input_seq,
                                             outputs_info=[initial_state])

        # hidden_states[-1] is the vector representation of the sentence
        return hidden_states

    def get_step_outputs(self, cur_word_vec, prev_hidden_state):
        return T.tanh(T.dot(cur_word_vec, self.input_weights)
                       + T.dot(prev_hidden_state, self.recurrent_weights)
                       + self.bias)

    def get_parameters(self):
        return [self.input_weights, self.recurrent_weights, self.bias]


class OutputLayer:

    def __init__(self, input_weight_init, bias_init):
        self.input_weights = theano.shared(input_weight_init())
        self.bias = theano.shared(bias_init())

    def get_outputs(self, inputs):
        non_linear_func = T.tanh
        return non_linear_func(T.dot(self.input_weights, inputs) + self.bias)

    def get_parameters(self):
        return [self.input_weights, self.bias]


def embedding_init(vocab_size):
    return np.random.randn(10, vocab_size)*0.01


def hidden_input_init():
    shape = (10, 50)
    a = np.random.normal(0.0, 1.0, shape)
    u, _, v = np.linalg.svd(a, full_matrices=False)
    q = u if u.shape == shape else v
    q = q.reshape(shape)
    return q


def hidden_recurrent_init():
    shape = (50, 50)
    a = np.random.normal(0.0, 1.0, shape)
    u, _, v = np.linalg.svd(a, full_matrices=False)
    q = u if u.shape == shape else v
    q = q.reshape(shape)
    return q

def output_input_init():
    shape = (50, 50)
    a = np.random.normal(0.0, 1.0, shape)
    u, _, v = np.linalg.svd(a, full_matrices=False)
    q = u if u.shape == shape else v
    q = q.reshape(shape)
    return q


def bias_init():
    return np.zeros(50)
    # return np.random.standard_normal(50)*0.01


if __name__ == '__main__':
    file = 'Data/en/qa1_single-supporting-fact_test.txt'

    corpus = process_corpus(file)

    corpus, word_indices = corpus_to_vecs(corpus)

    # test_text = corpus.next()

    vocab_size = len(corpus[0][0])

    ####

    embed_layer = EmbeddingLayer(embedding_init, vocab_size)

    rnn_layer = RNNLayer(hidden_input_init, hidden_recurrent_init, bias_init)

    out_layer = OutputLayer(output_input_init, bias_init)

    print('input', rnn_layer.input_weights.get_value().shape)

    print('recurrent', rnn_layer.recurrent_weights.get_value().shape)

    ####

    sym_sent = T.matrix()

    sym_embed = embed_layer.get_outputs(sym_sent)

    sym_hidden = rnn_layer.get_outputs(sym_embed)

    sym_output = out_layer.get_outputs(sym_hidden[-1])

    net_pass = theano.function(inputs=[sym_sent], outputs=[sym_output])

    for sent in corpus[:10]:
        result = net_pass(sent)
        print(result)



































    # cur_in = T.vector()
    #
    # in_weights = hidden_input_init(0)
    #
    # prev_in = T.vector()
    #
    # hidden_weights = hidden_recurrent_init(0)
    #
    # act = T.tanh(T.dot(cur_in, in_weights)
    #        + T.dot(prev_in, hidden_weights))
    #
    # cell = theano.function(inputs=[cur_in, prev_in], outputs=[act])
    #
    # in_vec = np.ones((10, ))
    #
    # hidden_vec = np.ones((50, ))
    #
    # print(in_vec)
    #
    # print(in_vec.shape)
    #
    # print(type(in_vec))
    #
    # result = cell(in_vec, hidden_vec)
    #
    # print(result[0].shape)
    #
    # print(result)


