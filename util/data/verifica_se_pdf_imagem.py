# coding: utf-8

import os
import sys

data_links = sys.argv[1]

#files = os.listdir(data_links)
#for emendas in os.listdir(data_links):
#    for folder in os.listdir(emendas):
#        if folder == "txt":
#            for files in os.listdir(folder):
#                print(files)


#if os.stat('somefile.txt').st_size == 0 || 'Document Outline' in open(data_links).read():
#    os.remove(data_links)

for subdir, dirs, files in os.walk(data_links):
    for file in files:
        file_path = os.path.join(subdir, file)
        if os.stat(file_path).st_size == 0 or 'Document Outline' in open(file_path).read():
            os.remove(file_path)
            print "Removing file: " + file_path


