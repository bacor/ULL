import theano
import theano.tensor as T

import numpy as np

from GRU_Layer import GRULayer


class EmbeddingLayer:

    def __init__(self, w_init, shape_dict):
        self.embedding_weights = theano.shared(w_init(shape_dict['encoder_embedding']))

    def get_outputs(self, inputs):
        result, _ = theano.scan(self.embed_vec, inputs)
        return result

    def embed_vec(self, row):
        return T.dot(row, self.embedding_weights)

    def get_parameters(self):
        return [self.embedding_weights]


class RNNLayer:

    def __init__(self, w_init, b_init, shape_dict, gru=False):
        self.input_weights = theano.shared(w_init(shape_dict['encoder_recurrent_input']))
        self.recurrent_weights = theano.shared(w_init(shape_dict['encoder_recurrent_self']))
        self.bias = theano.shared(b_init(shape_dict['encoder_recurrent_bias']))

        self.use_gru = gru
        if gru:
            self.reset_weights_in = theano.shared(w_init(shape_dict['encoder_reset_in']))
            self.reset_weights_self = theano.shared(w_init(shape_dict['encoder_reset_self']))
            self.update_weights_in = theano.shared(w_init(shape_dict['encoder_update_in']))
            self.update_weights_self = theano.shared(w_init(shape_dict['encoder_update_self']))

            self.gru_layer = GRULayer(iter(self.get_parameters()))
            self.activation_func = self.gru_layer.activation
        else:
            self.activation_func = self.get_step_outputs

    def get_outputs(self, input_seq):
        initial_state = T.zeros((self.input_weights.shape[1], ))
        hidden_states, updates = theano.scan(fn=self.activation_func,
                                             sequences=input_seq,
                                             outputs_info=[initial_state])

        # hidden_states[-1] is the vector representation of the sentence
        return hidden_states

    def get_step_outputs(self, cur_word_vec, prev_hidden_state):
        return T.tanh(T.dot(cur_word_vec, self.input_weights)
                       + T.dot(prev_hidden_state, self.recurrent_weights)
                       + self.bias)

    def get_parameters(self):
        if self.use_gru:
            return [self.input_weights, self.recurrent_weights, self.reset_weights_in, self.reset_weights_self,
                    self.update_weights_in, self.update_weights_self, self.bias]
        else:
            return [self.input_weights, self.recurrent_weights, self.bias]


class OutputLayer:

    def __init__(self, w_init, b_init, shape_dict):
        self.input_weights = theano.shared(w_init(shape_dict['encoder_out_input']))
        self.bias = theano.shared(b_init(shape_dict['encoder_out_bias']))

    def get_outputs(self, inputs):
        non_linear_func = T.tanh
        return non_linear_func(T.dot(inputs, self.input_weights) + self.bias)

    def get_parameters(self):
        return [self.input_weights, self.bias]


if __name__ == '__main__':
    from main_reverse import weight_init, bias_init

    V, d, h, c = 4, 7, 11, 15

    sent_len = 2

    shape_dict = dict(
        encoder_embedding=(V, d),

        encoder_recurrent_input=(d, h),
        encoder_recurrent_self=(h, h),
        encoder_reset_in=(d, h),
        encoder_reset_self=(h, h),
        encoder_update_in=(d, h),
        encoder_update_self=(h, h),

        encoder_out_input=(h, c),

        encoder_recurrent_bias=h,
        encoder_out_bias=c
    )

    embed_layer = EmbeddingLayer(weight_init, shape_dict)

    rnn_layer = RNNLayer(weight_init, bias_init, shape_dict, gru=False)

    out_layer = OutputLayer(weight_init, bias_init, shape_dict)

    inputs = T.matrix()

    embedded_inputs = embed_layer.get_outputs(inputs)

    hidden_states = rnn_layer.get_outputs(embedded_inputs)

    output = out_layer.get_outputs(hidden_states[-1])

    f = theano.function([inputs], output)

    rand_inds = [np.random.randint(0, V) for _ in range(sent_len)]

    print(rand_inds)

    sent_mat = np.asarray([[1 if i == rand_inds[w] else 0 for i in range(V)] for w in range(sent_len)])

    print(f(sent_mat))