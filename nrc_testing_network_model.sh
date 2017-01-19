#!/bin/bash
#-d nome_dataset
#-p file_parametri
#-m file_modello
#-o file_output
#-c file_code
dataset=
matrix_name=
min_size=
max_size=
name_experiment=
parameters=
model=
output=
code=

while getopts "d:m:n:p:o:" OPTION;

do
	case $OPTION in
		d)
			dataset=${OPTARG}
			;;
		o)
			output=${OPTARG}
			;;
		m)
			model=${OPTARG}
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
code=$(echo $model|cut -d '.' -f 1)"_code.txt"



echo "INFO: Format ""$dataset"" according to Theano tool..."	
python root/nrc_workspace/src/python/make_theano_testset.py $dataset $code
#python src/python/DL_main_train_channel.py "data/"$parameters "data/"$dataset

echo "INFO: Test classification model..."	
python -W ignore root/nrc_workspace/src/python/DL_main_test_channel.py $parameters $dataset $model $output $code

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


