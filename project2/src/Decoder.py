import theano
import theano.tensor as T

import numpy as np

from GRU_Layer import GRULayer


class Decoder:

    def __init__(self, embedding, recurrent_layer, out_layer, softmax):
        self.embedding = embedding
        self.recurrent_layer = recurrent_layer
        self.out_layer = out_layer
        self.softmax = softmax

    def get_outputs(self, sent_rep, train_inputs=None):
        if train_inputs is not None:
            return self.get_outputs_train(sent_rep, train_inputs)

        output_size = self.out_layer.recurrent_weights.shape[0]
        initial_state = T.tanh(T.dot(sent_rep, self.recurrent_layer.context_weights))
        initial_output = T.zeros((output_size, ))

        results, updates = theano.scan(
            fn=self.get_step_output,
            outputs_info=[
                dict(initial=initial_state),
                dict(initial=initial_output),
                None
            ],
            sequences=[],
            non_sequences=[sent_rep],
            n_steps=30
        )

        return results

    def get_step_output(self, previous_hidden_state, previous_output, sent_repr):
        current_hidden_state = self.recurrent_layer.activation_func(previous_output, previous_hidden_state, sent_repr)

        current_output = self.out_layer.get_outputs(current_hidden_state, previous_output, sent_repr)

        # get from dimension D to dimension V here
        de_embedded = T.dot(current_output, self.embedding.embedding_weights.T)

        current_softmax = self.softmax.get_outputs(de_embedded)

        stop_cond = T.eq(T.argmax(current_softmax),current_softmax.shape[0]-1)

        return [current_hidden_state, current_output, current_softmax], theano.scan_module.until(stop_cond)

    def get_outputs_train(self, sent_rep, train_inputs):
        initial_state = T.tanh(T.dot(sent_rep, self.recurrent_layer.context_weights))

        results, updates = theano.scan(
            fn=self.get_step_output_train,
            outputs_info=[
                dict(initial=initial_state),
                None
            ],
            sequences=[dict(input=train_inputs, taps=[-1])],
            non_sequences=[sent_rep])

        return results

    def get_step_output_train(self, previous_word, previous_hidden_state, sent_repr):
        embedded_prev_word = T.dot(previous_word, self.embedding.embedding_weights)

        current_hidden_state = self.recurrent_layer. \
                                activation_func(embedded_prev_word, previous_hidden_state, sent_repr)

        current_output = self.out_layer.get_outputs(current_hidden_state, embedded_prev_word, sent_repr)

        # get from dimension D to dimension V here
        de_embedded = T.dot(current_output, self.embedding.embedding_weights.T)

        current_softmax = self.softmax.get_outputs(de_embedded)

        return [current_hidden_state, current_softmax]


    def get_parameters(self):
        return self.recurrent_layer.get_parameters() +\
                self.out_layer.get_parameters() +\
                self.softmax.get_parameters()


class RecurrentLayer:
    def __init__(self, w_init, b_init, shape_dict, gru=False):
        self.input_weights = theano.shared(w_init(shape_dict['decoder_recurrent_input']))
        self.recurrent_weights = theano.shared(w_init(shape_dict['decoder_recurrent_self']))
        self.context_weights = theano.shared(w_init(shape_dict['decoder_recurrent_context']))
        self.bias = theano.shared(b_init(shape_dict['decoder_recurrent_bias']))

        self.use_gru = gru
        if gru:
            self.reset_weights_in = theano.shared(w_init(shape_dict['decoder_reset_in']))
            self.reset_weights_self = theano.shared(w_init(shape_dict['decoder_reset_self']))
            self.reset_weights_context = theano.shared(w_init(shape_dict['decoder_reset_context']))
            self.update_weights_in = theano.shared(w_init(shape_dict['decoder_update_in']))
            self.update_weights_self = theano.shared(w_init(shape_dict['decoder_update_self']))
            self.update_weights_context = theano.shared(w_init(shape_dict['decoder_update_context']))

            self.gru_layer = GRULayer(iter(self.get_parameters()))
            self.activation_func = self.gru_layer.activation
        else:
            self.activation_func = self.get_hidden_activation

    def get_hidden_activation(self, previous_output, previous_hidden_state, sent_repr):
        return T.tanh(
            T.dot(previous_output, self.input_weights) +
            T.dot(previous_hidden_state, self.recurrent_weights) +
            T.dot(sent_repr, self.context_weights)
            + self.bias
        )

    def get_parameters(self):
        if self.use_gru:
            return [self.input_weights, self.recurrent_weights, self.reset_weights_in, self.reset_weights_self,
                    self.update_weights_in, self.update_weights_self, self.bias,
                    self.context_weights, self.reset_weights_context, self.update_weights_context]
        else:
            return [self.input_weights, self.recurrent_weights, self.context_weights, self.bias]

class DecoderOutputLayer:

    def __init__(self, w_init, b_init, shape_dict):
        self.input_weights = theano.shared(w_init(shape_dict['decoder_out_input']))
        self.recurrent_weights = theano.shared(w_init(shape_dict['decoder_out_self']))
        self.sent_weights = theano.shared(w_init(shape_dict['decoder_out_repr']))
        self.bias = theano.shared(b_init(shape_dict['decoder_out_bias']))

    def get_outputs(self, current_hidden_state, previous_output, sent_repr):
        nonlinear_func = T.tanh
        return nonlinear_func(T.dot(current_hidden_state, self.input_weights) +
                T.dot(previous_output, self.recurrent_weights) +
                T.dot(sent_repr, self.sent_weights) +
                self.bias)

    def get_parameters(self):
        return [self.input_weights, self.recurrent_weights, self.sent_weights, self.bias]


class SoftmaxLayer:

    def __init__(self, w_init, b_init, shape_dict):
        self.input_weights = theano.shared(w_init(shape_dict['decoder_softmax']))
        self.bias = theano.shared(b_init(shape_dict['decoder_softmax_bias']))

    def get_outputs(self, input_vector):
        enum = T.exp(T.dot(input_vector, self.input_weights) + self.bias)

        mat_sum = np.float64(0)

        # denom, _ = theano.scan(
        #     fn=lambda accum, cur_val: accum + cur_val,
        #     sequences=[enum],
        #     outputs_info=[mat_sum]
        # )
        #
        # denom = denom[-1]

        denom = T.sum(enum)

        return enum/denom

    def get_parameters(self):
        return [self.input_weights]


def probs_to_word(prob_vec):
    return np.argmax(prob_vec)

c_dim = 50
h_dim = 10
y_dim = 21
v_dim = 21

w_in = lambda: np.ones((c_dim, h_dim))
w_self = lambda: np.ones((h_dim, h_dim))
w_y = lambda: np.ones((y_dim, h_dim))
w_bias1 = lambda: np.ones((h_dim,))
w_s = lambda: np.ones((h_dim, y_dim))
w_s_c = lambda: np.ones((c_dim, y_dim))
w_self_y = lambda: np.ones((y_dim, y_dim))
w_bias2 = lambda: np.ones((y_dim,))
w_soft = lambda: np.eye(v_dim)

if __name__ == '__main__':

    vocab_size = 4

    # layer sizes
    d, h, c, k, V = 10, 20, 50, 20, vocab_size

    init_shapes = dict(
        encoder_embedding=(d, vocab_size),
        encoder_RNN_input=(d, h),
        encoder_RNN_self=(h, h),
        encoder_out_input=(h, c),

        decoder_RNN_input=(c, k),
        decoder_RNN_self=(k, k),
        decoder_RNN_word=(V, k),
        decoder_out_input=(k, V),
        decoder_out_self=(V, V),
        decoder_out_repr=(c, V),
        decoder_softmax=(vocab_size, vocab_size),

        encoder_RNN_bias=h,
        encoder_out_bias=c,
        decoder_RNN_bias=k,
        decoder_out_bias=V
    )

    from main_reverse import weight_init, bias_init


    outlayer = DecoderOutputLayer(weight_init, bias_init, init_shapes)

    softmax = SoftmaxLayer(weight_init, bias_init, init_shapes)

    from Encoder import EmbeddingLayer

    embedding = EmbeddingLayer(weight_init, init_shapes)

    reclayer = RecurrentLayer(weight_init, bias_init, init_shapes)

    recurrent = Decoder(embedding, reclayer, outlayer, softmax)

    context_vector = T.vector()

    sent_len = T.scalar(dtype='int64')

    rec_out = recurrent.get_outputs((context_vector, sent_len))

    f = theano.function(inputs=[context_vector, sent_len], outputs=rec_out[2])

    act_c = np.ones((c_dim, ))

    act_len = 6

    res = f(act_c, act_len)

    print(res)

    print(len(res))

    print(len(res[0]))

    print('=='*10)

    for word_pos in res:
        print probs_to_word(word_pos),