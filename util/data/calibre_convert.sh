#!/bin/bash

DIR_DATA=$1

for f in $(ls $DIR_DATA/pdf/); do
   extension="${f##*.}"
   filename="${f%.*}"
   ebook-convert $DIR_DATA/pdf/$f $DIR_DATA/txt/$filename.txt
done
