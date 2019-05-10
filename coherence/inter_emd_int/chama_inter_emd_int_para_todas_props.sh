#!/bin/bash

DIR_DATA=$1

for folder in $(ls $DIR_DATA/); do
	for f in $(ls $DIR_DATA/$folder/txt/); do
		python3 inter_emd_int.py ../../../versoes-de-proposicoes/emendas/ ../languagemodel/vectors_skipgram_lei_aprovadas.bin ../teste1
	done
done
