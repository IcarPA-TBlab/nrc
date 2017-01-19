#classi = ['snoRNA','snRNA','rRNA','miRNA','scaRNA']
import sys

##classi = ['tRNA','miRNA','scaRNA','5_8S_rRNA','5S_rRNA','CD-box','HACA-box','ribozyme','leader','Intron_gpI','Intron_gpII','riboswitch','IRES']
classi = []
##foutput = open("matrix_eccb16_dataset_Rfam_42_theano.txt",'w')

finput = open("root/nrc_workspace/data/"+sys.argv[1])
foutput = open("root/nrc_workspace/data/"+sys.argv[1].split(".")[0]+"_theano.txt",'w')
##model = train.split(".")
##model = model[len(model)-2]
##model = model.split("/")
##model = model[len(model)-1]

linea = finput.readline()
cont = 0
while (linea != ""):
    riga = linea.strip("\r\n").split(",")
    label = riga[len(riga)-1]
    if (label in classi):
        num_label = classi.index(label)
    else:
        classi.append(label)
        num_label = classi.index(label)
    riga = riga[:len(riga)-1]
##    num_label = classi.index(label)
    for elem in riga:
        foutput.write(elem+",")
    foutput.write(str(num_label)+"\n")
    linea = finput.readline()
foutput.close()

foutput = open("root/nrc_workspace/data/"+sys.argv[1].split(".")[0]+"_code.txt",'w')
for elem in classi:
    foutput.write(elem+","+str(classi.index(elem))+"\n")
foutput.close()
