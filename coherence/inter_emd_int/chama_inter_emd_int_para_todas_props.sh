#!/bin/bash

#Pasta com as emendas
DIR_DATA=$1

python3 -c "from nltk import download;download('stopwords')"
for folder in $(ls $DIR_DATA/); do
        echo $DIR_DATA$folder
	python3 ../../coherence/inter_emd_int/inter_emd_int.py $DIR_DATA$folder ../../coherence/languagemodel/vectors_skipgram_lei_aprovadas.bin emendas_all_dist/

done
