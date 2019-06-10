#!/bin/bash

DIR_DATA=$1

for folder in $(ls $DIR_DATA/); do
	for f in $(ls $DIR_DATA/$folder/pdf/); do
		filename="${f%.*}"
		for g in $(ls $DIR_DATA/$folder/pdf/$f); do
		      ebook-convert $DIR_DATA/$folder/pdf/$f $DIR_DATA/$folder/txt/$filename.txt
                      fileSize=`wc -c $DIR_DATA/$folder/txt/$filename.txt | cut -d' ' -f1`
		      if [ $fileSize -lt 100 ] 
			  then
				echo $DIR_DATA/$folder/txt/$filename.txt
			  	rm $DIR_DATA/$folder/txt/$filename.txt
			  fi
		done
	done
done
