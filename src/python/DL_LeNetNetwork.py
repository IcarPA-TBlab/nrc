

import numpy

import theano
import theano.tensor as T
from theano.tensor.signal import downsample
from theano.tensor.nnet import conv

from DL_logistic_sgd import LogReg

from mlp import HiddenLayer

import LeNetConvPoolLayer as LNCPL

import pickle

class LeNetNetwork(object):
    def __init__( self,

        x, y,

        rng,
        out3Shape,
        learning_rate, n_epochs,
        nkerns, batch_size,
        nchannels, ishape,    
        dimKernel0, poolSize0,
        dimKernel1, poolSize1,
        out2Shape
        ):

##        print '... building the model' #--------------------------------------
        layer0_input = x.reshape( (batch_size, nchannels, ishape[0], ishape[1]) )
  
        # Construct the second convolutional pooling layer
        out0Shape=((ishape[0]-dimKernel0[0]+1)/poolSize0[0], (ishape[1]-dimKernel0[1]+1)/poolSize0[1] )
        
        self.layer0 = LNCPL.LeNetConvPoolLayer(rng, input=layer0_input,
                image_shape=(batch_size, nchannels, ishape[0], ishape[1]),
                filter_shape=(nkerns[0], nchannels, dimKernel0[0], dimKernel0[1]), poolsize=poolSize0)

        # Construct the second convolutional pooling layer
        out1Shape=((out0Shape[0]-dimKernel1[0]+1)/poolSize1[0] , (out0Shape[1]-dimKernel1[1]+1)/poolSize1[1]  )

        self.layer1 = LNCPL.LeNetConvPoolLayer(rng, input=self.layer0.output,
                image_shape=(batch_size, nkerns[0], out0Shape[0], out0Shape[1]),
                filter_shape=(nkerns[1], nkerns[0], dimKernel1[0], dimKernel1[1]), poolsize=poolSize1)

        # the HiddenLayer being fully-connected, 
        layer2_input = self.layer1.output.flatten(2)

        self.layer2 = HiddenLayer(rng, input=layer2_input, n_in=nkerns[1] * out1Shape[0] * out1Shape[1],
                             n_out=out2Shape, activation=T.tanh)

        # classify the values of the fully-connected sigmoidal layer
        self.layer3 = LogReg(input=self.layer2.output, n_in=out2Shape, n_out=out3Shape)

        # create a list of all model parameters to be fit by gradient descent
        self.params = self.layer3.params + self.layer2.params + self.layer1.params + self.layer0.params

#-------------------------------------------------------------------------------
    def errors(self, y):
        return self.layer3.errors(y)
#-------------------------------------------------------------------------------
    def getParams(self):
        return self.params
#-------------------------------------------------------------------------------
    def f_cost(self, y):
        # the cost we minimize during training is the NLL of the model
        return self.layer3.negative_log_likelihood(y)

#-------------------------------------------------------------------------------
    def f_grads(self, y):
        # create a list of gradients for all model parameters
        return T.grad(self.f_cost(y), self.params)

#-------------------------------------------------------------------------------
    def buildUpdates(self, learning_rate, y):
       # train_model is a function that updates the model parameters by SGD 
        updates = []
        for param_i, grad_i in zip(self.params, self.f_grads(y)):
            updates.append((param_i, param_i - learning_rate * grad_i))
        return updates

#-------------------------------------------------------------------------------
    def getOut(self):
        #self.x = xIn
        return self.layer3.y_pred

#-------------------------------------------------------------------------------
    def saveModel(self, nomeFile):
        out=open(nomeFile, "wb")
        pickle.dump(self.params, out, -1)
        out.close()
#-------------------------------------------------------------------------------
    def loadModel(self,nomeFile):
        inp=open(nomeFile, "rb")
        temp=pickle.load(inp)
        inp.close()

        W_l3, b_l3, W_l2, b_l2,  W_l1, b_l1, W_l0, b_l0=temp

        #print "in LeNet\n",W_l3.get_value()

        self.layer3.setParams(W_l3.get_value(), b_l3.get_value())
        self.layer2.setParams(W_l2.get_value(), b_l2.get_value())
        self.layer1.setParams(W_l1.get_value(), b_l1.get_value())
        self.layer0.setParams(W_l0.get_value(), b_l0.get_value())



