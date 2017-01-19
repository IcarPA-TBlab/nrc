import numpy

import theano
import theano.tensor as T
from theano.tensor.signal import downsample
from theano.tensor.nnet import conv

# LAYER DI CONVOLUZIONE E POOLING DELLA RETE LeNet


# check sulle dimensioni
def checklists(a,b):
    return len(a)==len(b) and len(a)==sum([1 for i,j in zip(a,b) if i==j])


class LeNetConvPoolLayer(object):
    """Pool Layer of a convolutional network """

    def __init__(self, rng, input, filter_shape, image_shape, poolsize=(2, 2)):
        """
        Allocate a LeNetConvPoolLayer with shared variable internal parameters.

        :type rng: numpy.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.dtensor4
        :param input: symbolic image tensor, of shape image_shape

        :type filter_shape: tuple or list of length 4
        :param filter_shape: (number of filters, num input feature maps,
                              filter height,filter width)
        nel nostro caso:
			number of filters ==1 (l'immagine ha solo un layer)
			num input feature maps, : numero di matrici w
            filter height	== 1 (si tratta di un vettore in ingresso)
            filter width	: dimensione del filtro

        :type image_shape: tuple or list of length 4
        :param image_shape: (batch size, num input feature maps,
                             image height, image width)
         nel nostro caso:
			batch size,  : grandezza del batch
			num input feature maps, : numero di matrici w      
            image height == 1 (si tratta di un vettore in ingresso)
            image width : dimensione della rappresentazione
                            

        :type poolsize: tuple or list of length 2        
        :param poolsize: the downsampling (pooling) factor (#rows,#cols)
         nel nostro caso : una dimensione e' 1 perche' si tratta di vettori

        """

        assert image_shape[1] == filter_shape[1]
        self.input = input

        # there are "num input feature maps * filter height * filter width"
        # inputs to each hidden unit
        fan_in = numpy.prod(filter_shape[1:])
        # each unit in the lower layer receives a gradient from:
        # "num output feature maps * filter height * filter width" /
        #   pooling size
        fan_out = (filter_shape[0] * numpy.prod(filter_shape[2:]) /
                   numpy.prod(poolsize))
        # initialize weights with random weights
        W_bound = numpy.sqrt(6. / (fan_in + fan_out))
        self.W = theano.shared(numpy.asarray(
            rng.uniform(low=-W_bound, high=W_bound, size=filter_shape),
            dtype=theano.config.floatX),
                               borrow=True)

        # the bias is a 1D tensor -- one bias per output feature map
        b_values = numpy.zeros((filter_shape[0],), dtype=theano.config.floatX)
        self.b = theano.shared(value=b_values, borrow=True)

        # convolve input feature maps with filters
        conv_out = conv.conv2d(input=input, filters=self.W,
                filter_shape=filter_shape, image_shape=image_shape)

        # downsample each feature map individually, using maxpooling
        pooled_out = downsample.max_pool_2d(input=conv_out,
                                            ds=poolsize, ignore_border=True)

        # add the bias term. Since the bias is a vector (1D array), we first
        # reshape it to a tensor of shape (1,n_filters,1,1). Each bias will
        # thus be broadcasted across mini-batches and feature map
        # width & height
        self.output = T.tanh(pooled_out + self.b.dimshuffle('x', 0, 'x', 'x'))

        # store parameters of this layer
        self.params = [self.W, self.b]


    def setParams(self, W_IN, b_IN):
    # controllo sulle dimensioni
        if (checklists(W_IN.shape, self.W.shape.eval()) and checklists([len(b_IN)], self.b.shape.eval())	):

            self.W.set_value(W_IN)
            self.b.set_value(b_IN)
            #self.W = theano.shared(value=W_IN, name='W', borrow=True)
            # initialize the baises b as a vector of n_out 0s
            #self.b = theano.shared(value=b_IN, name='b', borrow=True)
        else : 
            print "LeNetConvPoolLayer:Errore nelle dimensioni delle matrici passate"
            print "W(input) shape", W_IN.shape, "W shape", self.W.shape.eval()
            print "b(input) shape", len(b_IN), "b shape", self.b.shape.eval()
            
            
            
            
            
    
if __name__ == '__main__':
    rng = numpy.random.RandomState(23455)
    #sgd_optimization_mnist()   rng, input, filter_shape, image_shape, poolsize=(2, 2)

    ishape=(100,3,10,10)
    inp=numpy.zeros(ishape)
    filter_shape=(7,3,10,10)

    lr=LeNetConvPoolLayer( rng, inp, filter_shape, ishape, (2,2) )
	
    W_in=numpy.ones(filter_shape)
    b_in=numpy.ones((filter_shape[0]))
    lr.setParams(W_in, b_in)           
