#!/bin/bash
#-d nome_testset
#-f nome matrice feature model
#-o nome output

testset=
matrix_name=
output_name=


while getopts "d:o:f:" OPTION;

do
        case $OPTION in
                d)
                        testset=${OPTARG}
                        ;;
				o)
						output_name=${OPTARG}
						;;
                f)
                        matrix_name=${OPTARG}
                        ;;
        esac
done


        testset_name=$(echo $testset|cut -d '.' -f 1)
        name_folder="data/"$testset_name
echo "INFO: Create testset folder..."
if [ -d "/root/nrc_workspace/"$name_folder ]; then
       # echo "folder exists"
        rm -rf "/root/nrc_workspace/"$name_folder
fi

echo "INFO: Read fasta sequences..."
#Creo la directory che dovra' contenere i dati
#mkdir -p $name_folder"/testset"
mkdir -p "/root/nrc_workspace/"$name_folder


#$1 rappresenta il nome del testset, $2 la cartella di destinazione
java root/nrc_workspace/src/FastaSeqsSplitter_Rfam "/root/nrc_workspace/data/"$testset "/root/nrc_workspace/"$name_folder

echo "INFO: Predict ncRNA sequences secondary structure using IPknot tool..."
java root/nrc_workspace/src/FastaReader_Rfam "/root/nrc_workspace/"$name_folder


#$1parametro cartella sorgente
java root/nrc_workspace/src/BPSEQparser_Rfam "/root/nrc_workspace/"$name_folder

#variabile che contiene il nome del file .nel che contiene il merge di tutti i file.nel
#file_name="merged.nel"

#prendo max e min di moss dalla matrice delle feature, che sono gli ultimi due numeri del
sizes=$(echo $matrix_name|cut -d '.' -f 1)
IFS='_' read -a myarray <<< "$sizes"
myarraylen=${#myarray[@]}
maxMoSS=${myarray[myarraylen-2]}
minMoSS=${myarray[myarraylen-1]}

#controllo quali file nel sono stati prodotti
echo "INFO:  For each secondary structure, calculate the vector representation in the feature model..."	
COUNTER=1
rm /root/nrc_workspace/data/$testset_name/merged.nel
for f in /root/nrc_workspace/data/$testset_name/*.nel;  
	do java -cp root/nrc_workspace/src/moss.jar:. root/nrc_workspace/src/CreateVectorFromNELfile $f "/root/nrc_workspace/data/"$matrix_name $maxMoSS $minMoSS
	printf "+(""$COUNTER"")+"
	COUNTER=$[$COUNTER +1]
done
echo "...done."

#unisco i vettori rappresentativi delle sequenze di ingresso in un file .temp
#echo "+ unisco i vettori rappresentativi delle sequenze di ingresso e li sposto in data"
cat /root/nrc_workspace/data/$testset_name/*out_matrix.part > /root/nrc_workspace/data/$testset_name/$output_name".temp"

#creo un nuovo file, nel quale aggiungo l'etichetta ad ogni riga. Poi sposto il file in ./data
java root/nrc_workspace/src/SeqClassMerge "/root/nrc_workspace/data/"$testset_name/$output_name".temp" "/root/nrc_workspace/data/"$testset_name"/hashIdType"
cp /root/nrc_workspace/data/$testset_name/$output_name".txt" /root/nrc_workspace/data/$output_name

########################################################################
#$2 path dove creare i file out.nel e out.sln
#$3 il path dove trovare il file marged.nel
#$4 size massinmo
#$5 size minimo
#java -cp src/moss.jar:. src/FeatureMaker $name_folder $name_folder"/testset/"$file_name $max_size $min_size

#nome da dare alla matrice relativa all'esperimento
#name_experiment="$matrix_name""_""$testset_name"_"$max_size$min_size"


#$2 rappresenta il nome della matrice che voglio dare per l'esperimento
#$3 il path dove creare la matrice
#java src/SLN2MatrixConverter $name_experiment $name_folder
