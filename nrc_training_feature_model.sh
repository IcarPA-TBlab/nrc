#!/bin/bash
#-d nome_dataset
#-o nome feature matrix output
#-n size massimo
#-m size minimo

dataset=
matrix_name=
min_size=
max_size=
name_experiment=

while getopts "d:o:m:n:" OPTION;

do
	case $OPTION in
		d)
			dataset=${OPTARG}
			;;
		o)
			matrix_name=${OPTARG}
			;;
		m)
			min_size=${OPTARG}
			;;
		n)
			max_size=${OPTARG}
			;;
	esac
done

		
        dataset_name=$(echo $dataset|cut -d '.' -f 1)
	name_folder="data/"$dataset_name"_"$max_size"_"$min_size
echo "INFO: Create experiment folder..."
if [ -d "/root/nrc_workspace/"$name_folder ]; then
	#echo "Warning: directory  exists."
	rm -rf "/root/nrc_workspace/"$name_folder
fi

echo "INFO: Read fasta sequences..."
#Creo la directory che dovra' contenere i dati
mkdir -p "/root/nrc_workspace/"$name_folder"/dataset_test"


#$1 rappresenta il nome del dataset, $2 la cartella di destinazione
java root/nrc_workspace/src/FastaSeqsSplitter_Rfam "/root/nrc_workspace/data/"$dataset "/root/nrc_workspace/"$name_folder"/dataset_test"

echo "INFO: Predict ncRNA sequences secondary structure using IPknot tool..."
java root/nrc_workspace/src/FastaReader_Rfam "/root/nrc_workspace/"$name_folder"/dataset_test"


#$1parametro cartella sorgente 
java root/nrc_workspace/src/BPSEQparser_Rfam "/root/nrc_workspace/"$name_folder"/dataset_test"

#variabile che contiene il nome del file .nel che contiene il merge di tutti i file.nel
file_name="merged.nel"

echo "INFO: Extract graph features using MoSS tool..."	
#$2 path dove creare i file out.nel e out.sln
#$3 il path dove trovare il file marged.nel
#$4 size massinmo
#$5 size minimo
java -cp root/nrc_workspace/src/moss.jar:. root/nrc_workspace/src/FeatureMaker "/root/nrc_workspace/"$name_folder "/root/nrc_workspace/"$name_folder"/dataset_test/"$file_name $max_size $min_size 

#nome da dare alla matrice relativa all'esperimento
#name_experiment="$matrix_name""_""$dataset_name"_"$max_size"_"$min_size"
name_experiment="$matrix_name""_""$max_size"_"$min_size"

echo "INFO: Create the feature model and the vector representation of input ncRNA sequences."
#$2 rappresenta il nome della matrice che voglio dare per l'esperimento
#$3 il path dove creare la matrice
java root/nrc_workspace/src/SLN2MatrixConverter $name_experiment "/root/nrc_workspace/"$name_folder

cp "/root/nrc_workspace/""$name_folder""/""$name_experiment"".txt" "/root/nrc_workspace/data/""$name_experiment"".txt"
cp "/root/nrc_workspace/""$name_folder""/out.nel" "/root/nrc_workspace/data/""$name_experiment"".nel"

