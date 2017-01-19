import os
import yaml
import sys
import warnings

from DL_TRAIN_conv_mlp import evaluate_lenet5 as ev
warnings.filterwarnings("ignore")

##fileParametri = "parametri.txt"
fileParametri = sys.argv[1]
##train = os.listdir("../train_eccb_64")
train = sys.argv[2]
model = train.split(".")[0]
train = "root/nrc_workspace/data/"+model+"_theano.txt"

##npattern ={'phylum': 3, 'class': 6, 'order': 22, 'family': 65, 'genus': 393}
##test = os.listdir("./test")

with open("root/nrc_workspace/data/"+fileParametri,'r') as stream:
    dc=(yaml.load(stream))
    
#for elem in train:
##model = train.split(".")
##model = model[len(model)-2]
##model = model.split("/")
##model = model[len(model)-1]
nomeModello = "root/nrc_workspace/data/"+model+".pkl"
ln=ev(train, 
                    nomeModello, 
                    dc["out3shape"],
                    dc["learning_rate"], dc["n_epochs"],
                    dc["n_kerns"], dc["batch_size"],
                    dc["n_channels"],
                    dc["dimKernel0"], dc["poolSize0"],
                    dc["dimKernel1"], dc["poolSize1"],					
                    dc["out2Shape"])
