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
import cPickle
import gzip
import os
import sys
import time

import yaml
import numpy

import theano
import theano.tensor as T
from theano.tensor.signal import downsample
from theano.tensor.nnet import conv

#from logistic_sgd__RIC import LogisticRegression
import caricaDati as ld # <<<<<<<<<< CARICAMENTO DEL DATASET

from mlp import HiddenLayer

import LeNetConvPoolLayer as LNCPL

import DL_LeNetNetwork as LN


def checklists(a,b):
    return len(a)==len(b) and len(a)==sum([1 for i,j in zip(a,b) if i==j])

def work_lenet5(nomeModello, fileTest, fileOut, 
					out3Shape,
					learning_rate, n_epochs,
                    nkerns, batch_size,
					nchannels,
                    dimKernel0, poolSize0,
                    dimKernel1, poolSize1,					
					out2Shape):

    rng = numpy.random.RandomState(23455)

    #datasets = load_data(dataset)  # <<<<<<<<<< CARICAMENTO DEL DATASET
    test_set_labels, TEMP_test_set_x, TEMP_test_set_y =ld.LXYfromFile(fileTest)
    ishape=[1,len(TEMP_test_set_x[0])]
    test_set_x, test_set_y = ld.shared_dataset(TEMP_test_set_x, TEMP_test_set_y )

    # compute number of minibatches for training, validation and testing
    n_test_batches = test_set_x.get_value(borrow=True).shape[0]
    rest_batch = n_test_batches % batch_size #calcola gli elementi resto dei 
##    n_test_batches /= batch_size
    n_test_batches = 1
    batch_size = test_set_x.get_value(borrow=True).shape[0]
    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch
    x = T.matrix('x')   # the data is presented as rasterized images
    y = T.ivector('y')  # the labels are presented as 1D vector of
                        # [int] labels

##    print "... dati caricati",
    # DIMENSIONA IL MODELLO LASCIANO MOLTI PARAMETRI FAKE
    LeNet=LN.LeNetNetwork(x, y, rng,out3Shape,
								learning_rate, n_epochs,
								nkerns, batch_size,
								nchannels, ishape,    
								dimKernel0, poolSize0,
								dimKernel1, poolSize1,
								out2Shape 
        )

##    print "...caricato il modello"
    LeNet.loadModel(nomeModello)

    #print LeNet.getParams()[0].get_value()

    getOut=theano.function([index], LeNet.getOut(),
        givens={            
            x: test_set_x[index * batch_size: (index + 1) * batch_size]})


    # accoda tutti gli output unendo i minibatch
    output=[]
    target=[]
    for i in xrange(n_test_batches):
        out=getOut(i)
        ref=test_set_y[i * batch_size: (i + 1) * batch_size].eval()

        output = output + out.tolist()
        target = target + ref.tolist()

##    out = getOut(n_test_batches)
##    ref = test_set_y[n_test_batches:n_test_batches+rest_batch].eval()
##    output = output + out.tolist()
##    target = target + ref.tolist()

    # conta gli errori confrontando gli elementi della lista
    numErrori = 0
##    print "# label:output_rete:classe_reale"
##    for i in range(len(output)):
##        print test_set_labels[i][0], ":", output[i],":", target[i]
##        if output[i] != target[i]:
##            numErrori += 1

##    print "# label:output_rete:classe_reale"
    foutput = open(fileOut,'w')
    foutput.write("label,output_rete,classe_reale\n")
    for i in range(len(output)):
        foutput.write(test_set_labels[i]+","+str(output[i])+","+str(target[i])+"\n")
        if output[i] != target[i]:
            numErrori += 1
    foutput.close()

##    print "# numero errori", numErrori, "su ", len(output)




if __name__ == '__main__':
	fileTest = sys.argv[1]
	fileParametri = sys.argv[2]
	fileOut = sys.argv[3]
	with open(fileParametri, 'r') as stream:
		dc=(yaml.load(stream))
		
##    print 	"Test su file: ", 				fileTest, \
##			" del modello salvato in: ", 	dc["nome_file_modello"],  \
##			". File di Output: ", 			fileOut
	
	work_lenet5(dc["nome_file_modello"], fileTest, fileOut, 
				dc["out3Shape"],
				dc["learning_rate"],dc["n_epochs"],
				dc["n_kerns"], 		dc["batch_size"],
				dc["n_channels"], 	dc["ishape"],
				dc["dimKernel0"], 	dc["poolSize0"],
				dc["dimKernel1"], 	dc["poolSize1"],					
				dc["out2Shape"])





