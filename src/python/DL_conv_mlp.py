"""This tutorial introduces the LeNet5 neural network architecture
using Theano.  LeNet5 is a convolutional neural network, good for
classifying images. This tutorial shows how to build the architecture,
and comes with all the hyper-parameters you need to reproduce the
paper's MNIST results.


This implementation simplifies the model in the following ways:

 - LeNetConvPool doesn't implement location-specific gain and bias parameters
 - LeNetConvPool doesn't implement pooling by average, it implements pooling
   by max.
 - Digit classification is implemented with a logistic regression rather than
   an RBF network
 - LeNet5 was not fully-connected convolutions at second layer

References:
 - Y. LeCun, L. Bottou, Y. Bengio and P. Haffner:
   Gradient-Based Learning Applied to Document
   Recognition, Proceedings of the IEEE, 86(11):2278-2324, November 1998.
   http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf



IL PROGRAMMA E' RIADATTATO E COMMENTATO PER LA ELABORAZIONE
DELLE STRINGHE RAPPRESENTATIVE DELLE SEQUENZE


"""
#import cPickle
#import gzip
import os
import sys
import time

import numpy

import theano
import theano.tensor as T
#from theano.tensor.signal import downsample
#from theano.tensor.nnet import conv


import caricaDati as ld

#from mlp import HiddenLayer

#import LeNetConvPoolLayer as LNCPL

import DL_LeNetNetwork as LN

def evaluate_lenet5(learning_rate=0.05,
					n_epochs=200,
                    dataset="",
                    nkerns=[10, 20],
                    batch_size=10,

                    ishape=(1,256),
                    dimKernel0=(1,5),
                    poolSize0 = (1,2),

                    dimKernel1=(1,5),
					poolSize1=(1,2),
					
					out2Shape=500,
					
					out3Shape=41,
					
					nomeModello="nomeModello.pkl"
                    ):
    """ Demonstrates lenet on MNIST dataset

    :type learning_rate: float
    :param learning_rate: learning rate used (factor for the stochastic
                          gradient)

    :type n_epochs: int
    :param n_epochs: maximal number of epochs to run the optimizer

    :type K: int
    :param K : dimensione della rappresentazione

    :type dataset: string
    :param dataset: path to the dataset used for training /testing (MNIST here)

    :type nkerns: list of ints
    :param nkerns: number of kernels on each layer
    """

    rng = numpy.random.RandomState(23455)

    #datasets = load_data(dataset)  # <<<<<<<<<< CARICAMENTO DEL DATASET
    datasets=ld.load_data("TRAIN_seq_16S.txt", "TEST_seq_16S.txt", "VALID_seq_16S.txt")

    TEMP_train_set_x, TEMP_train_set_y = datasets[0]
    TEMP_test_set_x, TEMP_test_set_y = datasets[1]
    TEMP_valid_set_x, TEMP_valid_set_y = datasets[2]

    print TEMP_train_set_y.shape

    train_set_x, train_set_y = ld.shared_dataset(TEMP_train_set_x, TEMP_train_set_y )
    valid_set_x, valid_set_y = ld.shared_dataset(TEMP_valid_set_x, TEMP_valid_set_y )
    test_set_x, test_set_y = ld.shared_dataset(TEMP_test_set_x, TEMP_test_set_y )


    # compute number of minibatches for training, validation and testing
    n_train_batches = train_set_x.get_value(borrow=True).shape[0]
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0]
    n_test_batches = test_set_x.get_value(borrow=True).shape[0]
    n_train_batches /= batch_size
    n_valid_batches /= batch_size
    n_test_batches /= batch_size

    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch
    x = T.matrix('x')   # the data is presented as rasterized images
    y = T.ivector('y')  # the labels are presented as 1D vector of
                        # [int] labels

    # DIMENSIONA IL MODELLO
    LeNet=LN.LeNetNetwork(x, y, rng)



    # create a function to compute the mistakes that are made by the model
    test_model = theano.function([index], LeNet.errors(y),
             givens={
                x: test_set_x[index * batch_size: (index + 1) * batch_size],
                y: test_set_y[index * batch_size: (index + 1) * batch_size]})

    validate_model = theano.function([index], LeNet.errors(y),
            givens={
                x: valid_set_x[index * batch_size: (index + 1) * batch_size],
                y: valid_set_y[index * batch_size: (index + 1) * batch_size]})

    params=LeNet.getParams()

    # create a list of gradients for all model parameters
    #grads = T.grad(LeNet.f_cost(y), params)

    # train_model is a function that updates the model parameters by
    # SGD Since this model has many parameters, it would be tedious to
    # manually create an update rule for each model parameter. We thus
    # create the updates list by automatically looping over all
    # (params[i],grads[i]) pairs.
    updates = LeNet.buildUpdates(learning_rate, y)

    train_model = theano.function([index], LeNet.f_cost(y), updates=updates,
          givens={
            x: train_set_x[index * batch_size: (index + 1) * batch_size],
            y: train_set_y[index * batch_size: (index + 1) * batch_size]})


    getOut=theano.function([index], LeNet.getOut(),
        givens={
            x: train_set_x[index * batch_size: (index + 1) * batch_size]})

    ###############
    # TRAIN MODEL #-----------------------------------------------------
    ###############
    print '... training'
    # early-stopping parameters
    patience = 10000  # look as this many examples regardless
    patience_increase = 2  # wait this much longer when a new best is
                           # found
    improvement_threshold = 0.995  # a relative improvement of this much is
                                   # considered significant
    validation_frequency = min(n_train_batches, patience / 2)
                                  # go through this many
                                  # minibatche before checking the network
                                  # on the validation set; in this case we
                                  # check every epoch

    best_params = None
    best_validation_loss = numpy.inf
    best_iter = 0
    test_score = 0.
    start_time = time.clock()

    epoch = 0
    done_looping = False

    while (epoch < n_epochs) and (not done_looping):
        epoch = epoch + 1
        for minibatch_index in xrange(n_train_batches):

            iter = (epoch - 1) * n_train_batches + minibatch_index

            if iter % 100 == 0:
                print 'training @ iter = ', iter
            cost_ij = train_model(minibatch_index)

            if (iter + 1) % validation_frequency == 0:

                # compute zero-one loss on validation set
                validation_losses = [validate_model(i) for i
                                     in xrange(n_valid_batches)]
                this_validation_loss = numpy.mean(validation_losses)
                print('epoch %i, minibatch %i/%i, validation error %f %%' % \
                      (epoch, minibatch_index + 1, n_train_batches, \
                       this_validation_loss * 100.))

                # if we got the best validation score until now
                if this_validation_loss < best_validation_loss:

                    #improve patience if loss improvement is good enough
                    if this_validation_loss < best_validation_loss *  \
                       improvement_threshold:
                        patience = max(patience, iter * patience_increase)

                    # save best validation score and iteration number
                    best_validation_loss = this_validation_loss
                    best_iter = iter

                    # test it on the test set
                    test_losses = [test_model(i) for i in xrange(n_test_batches)]
                    test_score = numpy.mean(test_losses)
                    print(('     epoch %i, minibatch %i/%i, test error of best '
                           'model %f %%') %
                          (epoch, minibatch_index + 1, n_train_batches,
                           test_score * 100.))

            if patience <= iter:
                done_looping = True
                break

    end_time = time.clock()
    print('Optimization complete.')
    print('Best validation score of %f %% obtained at iteration %i,'\
          'with test performance %f %%' %
          (best_validation_loss * 100., best_iter + 1, test_score * 100.))
    print >> sys.stderr, ('The code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((end_time - start_time) / 60.))



    print "...salva la rete"
    LeNet.saveModel(nomeModello)

    # stampa l'output della rete
    for i in xrange(n_train_batches):
        out=getOut(i)
        print "stimato", out, "\n", "reale  ", train_set_y[i * batch_size: (i + 1) * batch_size].eval()



    # restituisce il modello addestrato
    return LeNet





if __name__ == '__main__':
    ln=evaluate_lenet5()





