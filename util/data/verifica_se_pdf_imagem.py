# coding: utf-8

import os
import sys

data_links = sys.argv[1]

#Itera sobre os txt gerados pelo calibre_convert.sh
for subdir, dirs, files in os.walk(data_links):
    for file in files:
        file_path = os.path.join(subdir, file)
        #Apaga os txts gerados por pfds que eram imagens
        if os.stat(file_path).st_size == 0 or 'Document Outline' in open(file_path).read():
            os.remove(file_path)
            print "Removing file: " + file_path


