import numpy
import theano
import theano.tensor as T

def LXYfromFile(filein):
	fin=open(filein, "r")
	buf=fin.readlines()
	fin.close()
	shuffle_data(buf)
	x=[]
	y=[]
	temp = []
	labels=[]

	for b in buf:

		riga = b.strip("\n").split(",")
		lb=riga[0]
		labels.append(lb)

		temp = riga[1:len(riga)-1]
		x.append([float(xx) for xx in temp])
		
		taxa = riga[len(riga)-1]
		y.append(float(taxa))

	

	
	data_x=numpy.asarray(x)
	data_y=numpy.asarray(y)


	return (labels, data_x, data_y )


def shuffle_data(data):
        numpy.random.shuffle(data)

def load_data(trainFile):
	train = LXYfromFile(trainFile)	
	return [train]

def shared_dataset(data_x, data_y, borrow=True):
	""" Function that loads the dataset into shared variables

	The reason we store our dataset in shared variables is to allow
	Theano to copy it into the GPU memory (when code is run on GPU).
	Since copying data into the GPU is slow, copying a minibatch everytime
	is needed (the default behaviour if the data is not in a shared
	variable) would lead to a large decrease in performance.
	"""

	shared_x = theano.shared(numpy.asarray(data_x,
								dtype=theano.config.floatX),
								borrow=borrow)

	shared_y = theano.shared(numpy.asarray(data_y,
								dtype=theano.config.floatX),
								borrow=borrow)

	return shared_x, T.cast(shared_y, 'int32')
