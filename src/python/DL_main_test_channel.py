import os
import yaml
import sys
import warnings

from DL_WORK_conv_mlp import work_lenet5 as wl
warnings.filterwarnings("ignore")
fileParametri = sys.argv[1]
##fileParametri = "parametri.txt"
##test = os.listdir("./test_500_6k")
##test = os.listdir("../test_eccb_64")
test = sys.argv[2]
model = sys.argv[3]
out = sys.argv[4]
code = sys.argv[5]

classi = {}
##model = model.replace("test","train")
test = test.split(".")[0]
test = test+"_theano.txt"

with open("/root/nrc_workspace/data/"+fileParametri,'r') as stream:
    dc=(yaml.load(stream))

## testa il modello con il test set    
ln=wl("/root/nrc_workspace/data/"+model, 
                    "/root/nrc_workspace/data/"+test,
                    "/root/nrc_workspace/data/"+out.split(".")[0]+".tmp",
                    dc["out3shape"],
                    dc["learning_rate"], dc["n_epochs"],
                    dc["n_kerns"], dc["batch_size"],
                    dc["n_channels"],
                    dc["dimKernel0"], dc["poolSize0"],
                    dc["dimKernel1"], dc["poolSize1"],					
                    dc["out2Shape"])


##inserisce le etichette letterali al posto di quelle numeriche nel file di uscita
fcode = open("/root/nrc_workspace/data/"+code)

linea = fcode.readline()
while (linea != ""):
    riga = linea.strip("\n").split(",")
    classi[riga[1]] = riga[0]
    linea = fcode.readline()

foutput = open("/root/nrc_workspace/data/"+out,'w')
finput = open("/root/nrc_workspace/data/"+out.split(".")[0]+".tmp")

linea = finput.readline()
foutput.write(linea)
linea = finput.readline()
while (linea != ""):
    riga = linea.strip("\n").split(",")
    seq_id = riga[0]
    pred = riga[1]
    true = riga[2]
    foutput.write(seq_id+","+classi[pred]+","+classi[true]+"\n")
    linea = finput.readline()
foutput.close()
