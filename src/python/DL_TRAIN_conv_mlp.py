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
import yaml
import os
import sys
import time

import numpy

import theano
import theano.tensor as T

import caricaDati as ld

import DL_LeNetNetwork as LN

def evaluate_lenet5(nomeTrain, 
					nomeModello, 
					
					out3Shape,
					learning_rate, n_epochs,
                    nkerns, batch_size,
					nchannels,
                    dimKernel0, poolSize0,
                    dimKernel1, poolSize1,					
					out2Shape			
                    ):


    rng = numpy.random.RandomState(23455)

    # CARICAMENTO DEL DATASET
    datasets=ld.load_data(nomeTrain)

    train_set_labels, TEMP_train_set_x, TEMP_train_set_y = datasets[0]
    ishape=[1,len(TEMP_train_set_x[0])]
    train_set_x, train_set_y = ld.shared_dataset(TEMP_train_set_x, TEMP_train_set_y )

    # compute number of minibatches for training
    n_train_batches = train_set_x.get_value(borrow=True).shape[0]

    n_train_batches /= batch_size

    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch
    x = T.matrix('x')   # the data is presented as rasterized images
    y = T.ivector('y')  # the labels are presented as 1D vector of
                        # [int] labels

    # DIMENSIONA IL MODELLO
    LeNet=LN.LeNetNetwork( 
		x,y,
        rng,
        
        out3Shape,        
        learning_rate,  n_epochs,
        nkerns,  batch_size,
        nchannels,  ishape,        
        dimKernel0,  poolSize0,
        dimKernel1,  poolSize1,
        out2Shape)

    updates = LeNet.buildUpdates(learning_rate, y)

    train_model = theano.function([index], LeNet.f_cost(y), updates=updates,
          givens={
            x: train_set_x[index * batch_size: (index + 1) * batch_size],
            y: train_set_y[index * batch_size: (index + 1) * batch_size]})


##    print "... training" #----------------------------------------------------

    start_time = time.clock()

    epoch = 0

    while (epoch < n_epochs) :
        epoch = epoch + 1
        for minibatch_index in xrange(n_train_batches):

            train_model(minibatch_index)

            iter = (epoch - 1) * n_train_batches + minibatch_index

        sys.stdout.write('+')
        sys.stdout.flush()
    print ".. done."
##    print "...salva la rete"
    LeNet.saveModel(nomeModello)

    # restituisce il modello addestrato
    return LeNet





if __name__ == '__main__':
    fileParametri  = sys.argv[1]
    
    with open(fileParametri, 'r') as stream:
		dc=(yaml.load(stream))
    
    print "Addestramento su file: ", dc["nome_file_training"], "File Parametri: ", fileParametri, "Modello salvato in: ", dc["nome_file_modello"]
    
    ln=evaluate_lenet5(	dc["nome_file_training"], 
						dc["nome_file_modello"], 
					
						dc["out3Shape"],
						dc["learning_rate"], dc["n_epochs"],
						dc["n_kerns"], dc["batch_size"],
						dc["n_channels"], dc["ishape"],
						dc["dimKernel0"], dc["poolSize0"],
						dc["dimKernel1"], dc["poolSize1"],					
						dc["out2Shape"])





