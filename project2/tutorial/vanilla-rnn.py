import random
import itertools
import numpy as np

x = []
y = []
for i in xrange(1, 50):
    x.append([0] * i)
    y.append(0)
    k = random.randint(0, len(x[-1]) - 1)
    x.append(list(x[-1]))
    x[-1][k] = 1
    y.append(1)

zipped = zip(x, y)
random.shuffle(zipped)
x, y = zip(*zipped)
n = int(0.9 * len(zipped))

train_x, train_y = x[:n], y[:n]
test_x, test_y = x[n:], y[n:]


######################################


import theano
from theano import tensor as T


class EmbeddingLayer(object):
    def __init__(self, embedding_init):
        self.embedding_matrix = theano.shared(embedding_init())

    def get_output_expr(self, input_expr):
        return self.embedding_matrix[input_expr]

    def get_parameters(self):
        return [self.embedding_matrix]


class RnnLayer(object):
    def __init__(self, w_init, u_init):
        self.W = theano.shared(w_init())
        self.U = theano.shared(u_init())

    def get_output_expr(self, input_sequence):
        h0 = T.zeros((self.W.shape[0], ))

        h, _ = theano.scan(fn=self.__get_rnn_step_expr,
                           sequences=input_sequence,
                           outputs_info=[h0])
        return h

    def __get_rnn_step_expr(self, x_t, h_tm1):
        return T.tanh(T.dot(h_tm1, self.W) + T.dot(x_t, self.U))

    def get_parameters(self):
        return [self.W, self.U]

    
class LogisticRegresion(object):
    def __init__(self, w_init):
        self.W = theano.shared(w_init())
        
    def get_output_expr(self, input_expr):
        pre_softmax_expr = T.dot(input_expr, self.W)
        return 1 / (1 + T.exp(pre_softmax_expr))

    def get_parameters(self):
        return [self.W]
    

def get_sgd_updates(cost, params, lr=0.01):
    grads = T.grad(cost=cost, wrt=params)
    updates = []
    for p, g in zip(params, grads):
        updates.append([p, p - lr * g])
    return updates 


######################################


def embedding_init():
    return np.random.randn(2, 30) * 0.01


def w_init():
    shape = (50, 50)
    a = np.random.normal(0.0, 1.0, shape)
    u, _, v = np.linalg.svd(a, full_matrices=False)
    q = u if u.shape == shape else v
    q = q.reshape(shape)
    return q


def u_init():
    shape = (30, 50)
    a = np.random.normal(0.0, 1.0, shape)
    u, _, v = np.linalg.svd(a, full_matrices=False)
    q = u if u.shape == shape else v
    q = q.reshape(shape)
    return q


def lr_init():
    return np.random.randn(50, ) * 0.01  
    

######################################


embedding_layer = EmbeddingLayer(embedding_init)
rnn_layer = RnnLayer(w_init, u_init)
lr_layer = LogisticRegresion(lr_init)

x = T.ivector()
y = T.iscalar()

embedding_expr = embedding_layer.get_output_expr(x)
h = rnn_layer.get_output_expr(embedding_expr)
py_x = lr_layer.get_output_expr(h[-1])
y_pred = py_x > 0.5
cost = - y * T.log(py_x) - (1 - y) * T.log(1 - py_x)
updates = get_sgd_updates(cost, embedding_layer.get_parameters() + rnn_layer.get_parameters() + lr_layer.get_parameters())
train = theano.function(inputs=[x, y], outputs=[cost, y_pred], updates=updates)
val = theano.function(inputs=[x, y], outputs=[cost, y_pred]) 
    

######################################


c = []
acc = []
for i in xrange(200):
    for x_datum, y_datum in zip(train_x, train_y):
        a, b = train(x_datum, y_datum)
        c.append(a)
        acc.append(b == y_datum)
    if i % 10 == 0:
        print 'train', np.mean(c), np.mean(acc)
        c = []
        acc = []
        for x_datum, y_datum in zip(test_x, test_y):
            a, b = val(x_datum, y_datum)
            c.append(a)
            acc.append(b == y_datum)
        print 'val', np.mean(c), np.mean(acc)
        print '=' * 10