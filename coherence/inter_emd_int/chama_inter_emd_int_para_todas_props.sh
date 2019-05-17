#!/bin/bash

#Pasta com as emendas
DIR_DATA=$1

for folder in $(ls $DIR_DATA/); do
        echo $DIR_DATA$folder
	python3 ../../coherence/inter_emd_int/inter_emd_int.py $DIR_DATA$folder ../../coherence/languagemodel/vectors_skipgram_lei_aprovadas.bin ../teste1
done
