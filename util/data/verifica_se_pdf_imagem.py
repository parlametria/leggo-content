# coding: utf-8

import os
import sys

data_links = sys.argv[1]

#Itera sobre os txt gerados pelo calibre_convert.sh
f = open("log_arquivos_removidos_imagens.txt","w+")
for subdir, dirs, files in os.walk(data_links):
    for file in files:
        file_path = os.path.join(subdir, file)
        #Apaga os txts gerados por pfds que eram imagens
        if os.stat(file_path).st_size < 100:
            os.remove(file_path)
            print "Removing file: " + file_path
            f.write("Removing file: " + file_path + "\r\n")


