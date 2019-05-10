#!/bin/bash

DIR_DATA=$1

for folder in $(ls $DIR_DATA/); do
	for f in $(ls $DIR_DATA/$folder/pdf/); do
		extension="${f##*.}"
		filename="${f%.*}"
		for g in $(ls $DIR_DATA/$folder/pdf/$f); do
		      extension="${g##*.}"
		      ebook-convert $DIR_DATA/$folder/pdf/$f $DIR_DATA/$folder/txt/$filename.txt
                      python verifica_se_pdf_imagem.py $DIR_DATA/$folder/txt/$filename.txt
		done
	done
done
