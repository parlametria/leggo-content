#!/bin/bash

DIR_DATA=$1

for f in $(ls $DIR_DATA/pdf/); do
   extension="${f##*.}"
   filename="${f%.*}"
   for g in $(ls $DIR_DATA/pdf/$f/pdf/); do
      extension="${g##*.}"
      filename="${g%.*}"
      ebook-convert $DIR_DATA/pdf/$f/pdf/$g $DIR_DATA/txt/$filename.txt
   done
done
