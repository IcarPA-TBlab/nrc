### nRC: non-coding RNA Classification Tool
A tool for classification of ncRNA sequences based on structural features extracted from RNA secondary structure and a deep learning architecture implementing a convolutional neural network.

#### Dependences:
* Python (2.7.5)
* Theano (0.8.2)
* NumPy  (1.11.2)
* Pyyaml (3.12)
* Java JDK  (1.8.0)
* ViennaRNA (1.8.5)
* Ipknot (0.0.2)
* GLPK	(4.60)

### nRC tool docker image:
https://hub.docker.com/r/tblab/nrc/


### How to Use
The best way to use nRC tool is to create a container from the docker image above. 
Anyway, it is possible to download source code, install all dependences and execute the following steps.

#### nRC Training process
##### Step 1: training feature model
```console
nrc_training_feature_model.sh -d <nRNA_training_file>.fasta -o <experiment_name> -n <graph_feature_max_size> -m <graph_feature_min_size>
```
##### Step 2: traning CNN (create classification model)
```console
nrc_training_network_model.sh -d <experiment_name>_<graph_feature_max_size>_<graph_feature_min_size>.txt -p <parameters>
```

####   
#### nRC Testing process

##### Step 3: testing feature model
```console
nrc_testing_feature_model.sh -d <nRNA_testing_file>.fasta  -f <experiment_name>_<graph_feature_max_size>_<graph_feature_min_size>.nel -o <sequence_output_name>
```
##### Step 4: testing CNN (test classification model)
```console
nrc_testing_network_model.sh -d <sequence_output_name> -p <parameters> -m <experiment_name>_<graph_feature_max_size>_<graph_feature_min_size>.pkl -o <classification_output_name>
```
###
### Datasets
This distribution contains two datasets. Both of them are available in "__data__" folder. 
* The "__sample__" datases is a small dataset with 40 ncRNA fasta sequences (belonging to 4 ncRNA classes) for training and 20 ncRNA fasta sequences for testing.
* The "__ECCB2017__" dataset has been used for experiments in the manuscript submitted at ECCB2017 conference. It is composed by a training file with 6320 ncRNA fasta sequences (belonging to 13 ncRNA classes) and two validated file with respectively 2600 fasta sequences (13 classes) and 2400 ncRNA fasta sequences (12 classes). All of them are extracted from Rfam database. 
nRC trained models used in the manuscript submitted at ECCB2017 conference are available at http://tblab.pa.icar.cnr.it/public/nRC/ECCB2017_dataset/
