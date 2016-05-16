import theano
import theano.tensor as T

import numpy as np

class GRULayer:
    def __init__(self, initial_weights):
        self.input_weights = next(initial_weights)
        self.recurrent_weights = next(initial_weights)
        self.reset_weights_in = next(initial_weights)
        self.reset_weights_self = next(initial_weights)
        self.update_weights_in = next(initial_weights)
        self.update_weights_self = next(initial_weights)
        self.bias = next(initial_weights)
        try:
            self.input_weights_context = next(initial_weights)
            self.reset_weights_context = next(initial_weights)
            self.update_weights_context = next(initial_weights)
        except StopIteration:
            pass

    def activation(self, emb_word, h_prev_t, context=None):
        if context is None:
            update = T.nnet.sigmoid(T.dot(emb_word, self.update_weights_in) +
                     T.dot(h_prev_t, self.update_weights_self))

            reset = T.nnet.sigmoid(T.dot(emb_word, self.reset_weights_in) +
                                   T.dot(h_prev_t, self.reset_weights_self))

            h_cur = T.tanh(T.dot(emb_word, self.input_weights) +
                           T.dot(reset * h_prev_t, self.recurrent_weights) + self.bias)
        else:
            u1 = T.dot(emb_word, self.update_weights_in)
            u2 = T.dot(h_prev_t, self.update_weights_self)
            u3 = T.dot(context, self.update_weights_context)
            update = T.nnet.sigmoid(u1 +
                                u2 + u3)

            reset = T.nnet.sigmoid(T.dot(emb_word, self.reset_weights_in) +
                                T.dot(h_prev_t, self.reset_weights_self) + T.dot(context, self.reset_weights_context))

            h_cur = T.tanh(T.dot(emb_word, self.input_weights) +
                           reset*(T.dot(h_prev_t, self.recurrent_weights) +
                           T.dot(context, self.input_weights_context)) + self.bias)

        current_state = update * h_prev_t + (1 - update) * h_cur

        return current_state


