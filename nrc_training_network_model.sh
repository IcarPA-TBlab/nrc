#!/bin/bash
#-d nome_dataset
#-M nome matrice
#-n size massimo
#-m size minimo
#-p file_parametri

dataset=
matrix_name=
name_experiment=
parameters=

while getopts "d:M:p:" OPTION;

do
	case $OPTION in
		d)
			dataset=${OPTARG}
			;;
		M)
			matrix_name=${OPTARG}
			;;
		p)
			parameters=${OPTARG}
			;;
	esac
done

		
#        dataset_name=$(echo $dataset|cut -d '.' -f 1)
#	name_folder="data/"$dataset_name"_"$max_size$min_size

#if [ -d $name_folder ]; then
#	echo "esiste"
#	rm -rf $name_folder
#fi
echo "INFO: Format ""$dataset"" according to Theano tool..."	
python root/nrc_workspace/src/python/make_theano_dataset.py $dataset
#python src/python/DL_main_train_channel.py "data/"$parameters "data/"$dataset

echo "INFO: Train a CNN deep learning classification model..."	
python -W ignore root/nrc_workspace/src/python/DL_main_train_channel.py $parameters $dataset

#Creo la directory che dovra' contenere i dati
#mkdir -p $name_folder"/dataset_test"


#$1 rappresenta il nome del dataset, $2 la cartella di destinazione
#java src/FastaSeqsSplitter_Rfam "data/"$dataset $name_folder"/dataset_test"

#java src/FastaReader_Rfam $name_folder"/dataset_test"


#$1parametro cartella sorgente 
#java src/BPSEQparser_Rfam $name_folder"/dataset_test"

#variabile che contiene il nome del file .nel che contiene il merge di tutti i file.nel
#file_name="merged.nel"

	
#$2 path dove creare i file out.nel e out.sln
#$3 il path dove trovare il file marged.nel
#$4 size massinmo
#$5 size minimo
#java -cp src/moss.jar:. src/FeatureMaker $name_folder $name_folder"/dataset_test/"$file_name $max_size $min_size 

#nome da dare alla matrice relativa all'esperimento
#name_experiment="$matrix_name""_""$dataset_name"_"$max_size$min_size"	


#$2 rappresenta il nome della matrice che voglio dare per l'esperimento
#$3 il path dove creare la matrice
#java src/SLN2MatrixConverter $name_experiment $name_folder


