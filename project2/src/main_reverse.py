from Get_Input_Reverse import process_corpus, corpus_to_vecs
from Encoder import *
from Decoder import *


def weight_init(shape):
    a = np.random.normal(0.0, 1.0, shape)
    u, _, v = np.linalg.svd(a, full_matrices=False)
    q = u if u.shape == shape else v
    q = q.reshape(shape)
    return q


def bias_init(layer_size):
    return np.asarray([np.random.randn() for _ in range(layer_size)])


def get_cost(prob_mat, true_indices):
    # reverse indices!!!
    # first element of vector is start symbol, last element is end symbol -> stay in their places
    reverse_indices = T.concatenate([true_indices[0:1], true_indices[-2:0:-1], true_indices[-1:]])

    single_neg_llhood = lambda row, ind: -T.log(T.dot(row, ind))

    probs, _ = theano.scan(
        fn=single_neg_llhood,
        sequences=[prob_mat, reverse_indices]
    )

    return T.sum(probs)

def get_sdg_updates(cost, params, learn_rate=0.01):
    grads = T.grad(cost=cost, wrt=params)
    updates = []
    for p, g in zip(params, grads):
        updates.append([p, p - learn_rate * g])
    return updates


def one_hot_to_index(vec):
    return [i for i, item in enumerate(vec) if item == 1][0]



# TODO:
# x restructure random intialisations
# x take care of biases (have different initialisation technique)
# x add end of sentence markers
# x get rid of sentence length parameter -> stop outputting words when network produces EOF marker
# x get from word probabilities to words
# x de-embed vectors before softmax
# - implement training
# - make flag for training and running
# - during training:
#   -> give true sentence length
#   -> give true last word to decoder outputlayer
# - during testing:
#   -> produce words until EOL is produced
#   -> give last output of outputlayer to outputlayer


def training():
    sym_sent = T.matrix()
    embedded_sent = embed_layer.get_outputs(sym_sent)
    en_hidden_state = en_rnn_layer.get_outputs(embedded_sent)
    context_vector = en_out_layer.get_outputs(en_hidden_state[-1])
    de_hidden_states, de_softmax = decoder.get_outputs(context_vector, sym_sent)
    cost = get_cost(de_softmax, sym_sent)
    updates = get_sdg_updates(cost, embed_layer.get_parameters() + en_rnn_layer.get_parameters() +
                              en_out_layer.get_parameters() + decoder.get_parameters())
    train = theano.function(inputs=[sym_sent], outputs=[cost, de_softmax], updates=updates)

    return train


def testing():
    sym_sent = T.matrix()
    embedded_sent = embed_layer.get_outputs(sym_sent)
    en_hidden_state = en_rnn_layer.get_outputs(embedded_sent)
    context_vector = en_out_layer.get_outputs(en_hidden_state[-1])
    de_hidden_states, de_out_states, de_softmax = decoder.get_outputs(context_vector)
    cost = get_cost(de_softmax, sym_sent)
    net_pass = theano.function(inputs=[sym_sent], outputs=[cost, de_softmax])
    return net_pass




if __name__ == '__main__':
    file = 'Data/en/qa1_single-supporting-fact_test.txt'

    corpus = process_corpus(file)

    corpus, word_indices = corpus_to_vecs(corpus)

    vocab_size = len(corpus[0][0])

    ####

    # layer sizes
    d, h, c, k = 10, 27, 50, 23

    init_shapes = dict(
        encoder_embedding=(vocab_size, d),
        encoder_recurrent_input=(d, h),
        encoder_recurrent_self=(h, h),
        encoder_out_input=(h, c),

        decoder_recurrent_input=(d, k),
        decoder_recurrent_self=(k, k),
        decoder_recurrent_context=(c, k),
        decoder_out_input=(k, d),
        decoder_out_self=(d, d),
        decoder_out_repr=(c, d),
        decoder_softmax=(vocab_size, vocab_size),

        encoder_recurrent_bias=h,
        encoder_out_bias=c,
        decoder_recurrent_bias=k,
        decoder_out_bias=d,
        decoder_softmax_bias=vocab_size
    )
    # T.dot((c, ), (d, k))
    encoder_gru_shapes = dict(
        encoder_reset_in=(d, h),
        encoder_reset_self=(h, h),
        encoder_update_in=(d, h),
        encoder_update_self=(h, h)
    )

    decoder_gru_shapes = dict(
        decoder_reset_in=(d, k),
        decoder_reset_self=(k, k),
        decoder_update_in=(d, k),
        decoder_update_self=(k, k),
        decoder_reset_context=(c, k),
        decoder_update_context=(c, k)
    )
    init_shapes.update(encoder_gru_shapes)

    init_shapes.update(decoder_gru_shapes)

    theano.config.optimizer = 'None'

    embed_layer = EmbeddingLayer(weight_init, init_shapes)

    en_rnn_layer = RNNLayer(weight_init, bias_init, init_shapes, gru=True)

    en_out_layer = OutputLayer(weight_init, bias_init, init_shapes)

    reclayer = RecurrentLayer(weight_init, bias_init, init_shapes, gru=True)

    de_out_layer = DecoderOutputLayer(weight_init, bias_init, init_shapes)

    softmax = SoftmaxLayer(weight_init, bias_init, init_shapes)

    decoder = Decoder(embed_layer, reclayer, de_out_layer, softmax)

    ####

    train_sent = training()

    pass_sent = testing()

    for i in range(21):
        overall_cost = 0
        for sent in corpus[:-100]:
            result = train_sent(sent)
            overall_cost += result[0]
            if i % 20 == 0:
                print
                print('cost:', result[0])
                print([one_hot_to_index(v) for v in sent])
                print([probs_to_word(v) for v in result[1]])
                print('='*10)
        if i % 2 == 0:
            print
            print('*'*10)
            print(i)
            print('data cost:', overall_cost)
            print('*' * 10)

    print('==='*10)
    print('==='*10)
    print('==='*10)
    print('TESTING')

    overall_cost = 0
    for sent in corpus[2900:]:
        result = pass_sent(sent)
        overall_cost += result[0]
        print('cost:', result[0])
        print([one_hot_to_index(v) for v in sent])
        print([probs_to_word(v) for v in result[1]])
        print('=' * 5)

    print('data cost:', overall_cost)
