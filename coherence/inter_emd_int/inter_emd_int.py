
# coding: utf-8

# In[8]:

import re
from nltk.corpus import stopwords
from nltk import download
from string import punctuation
import os
from gensim.models import KeyedVectors
import numpy as np
import math
import sys
from pathlib import Path


download('stopwords')


# In[9]:


import pandas as pd


# In[10]:

# Argumentos que o programa deve receber:
# -1º: Path para pasta onde estão os textos das emendas extraídas
# -2º: Path para o arquivo .bin do modelo Word2Vec treinado 
# -3º: Path para a pasta onde a tabela de features deve ser salva
# -4º: Path para o arquivo Inteiro Teor


emdPath = sys.argv[1]
modelPath = sys.argv[2]
outputPath = sys.argv[3]
intPath = sys.argv[4]

# =============================================================================
# Paths para teste
# emdPath = Path('../mpv870/teste')
# modelPath = Path('../languagemodel/vectors_skipgram_lei_aprovadas.bin')
# outputPath = Path('../teste1')
# intPath = Path('../mpv870/inteiroteor/inteiroteor.pdf.txt')
# =============================================================================

files = os.listdir(emdPath)

files = [value for value in files if len(value.split('.DS_Store'))==1]

means = []
variances=[]
stds = []
sqdmeans = []
totdists = []
model = KeyedVectors.load_word2vec_format(modelPath, binary=True)




# # Intercoerência

# In[11]:

# Lista de Sentenças de cada emenda
    
emdSentences = []
finalTokenizedSentences = []
for file in files:
    file = open(emdPath + '/' + str(file), 'r', encoding = 'UTF8')
    line = file.read()
    tokenized_sentences = []
    line = re.sub(r'[^\w\d\s]+', '', line)
    tokenized_sentences.append(line.lower().split())
    stop_words = set(stopwords.words('portuguese') + list(punctuation))
    for t in tokenized_sentences:
        emdSentences.append([w for w in t if w not in stop_words])



# Lista de sentenças do inteiro teor
    
intFile = open(intPath, 'r', encoding = 'UTF8')
# =============================================================================
# lines = intFile.readlines()
# =============================================================================


finalTokenizedSentences = []
intSentences = []
for line in intFile:
    tokenized_sentences = []
    line = re.sub(r'[^\w\d\s]+', '', line)
    tokenized_sentences.append(line.lower().split())
    stop_words = set(stopwords.words('portuguese') + list(punctuation))
    for t in tokenized_sentences:
        intSentences.append([w for w in t if w not in stop_words])



# In[12]:


means = []
variances=[]
stds = []
sqdmeans = []
totdists = []
num = 0

allDists = []
indexes = []

for emd,i in zip(emdSentences,files):
    print("abrindo emenda:",i.split('.txt')[0])
    distances = []
    
    for teor,j in zip(intSentences,range(len(intSentences))):
        
        if len(emd) > 4 and len(teor)> 4:
            d = model.wmdistance(emd,teor)
            # Distância para calcular a média
            distances.append(d)
            # dists é uma lista de todas as distâncias calculadas
            indexes.append('_'.join([i, str(j)]))
            
    distances = np.array(distances)
    distances[distances > 1e308] = 0
    distances = distances/np.sqrt((distances**2).sum())
    

    allDists.extend(distances)
    mean = distances.mean()
    var = distances.var()
    std = math.sqrt(distances.var())
    sqdmean = 0    
        
    if len(distances) != 0:
        for i in distances:
            sqdmean+=i**2
        sqdmean = sqdmean/len(distances)
    totdist = distances.sum()

    means.append(mean)
    variances.append(var)
    stds.append(std)
    sqdmeans.append(sqdmean)
    totdists.append(totdist)
    num +=1

allDists = np.array(allDists)

indexes = np.array(indexes)

df = pd.DataFrame(np.column_stack([files, means, variances, stds, sqdmeans, totdists]), 
                  columns=['files','mean_distance', 'variance', 'standard_deviation', 'sqd_means', 'total_distances']).to_csv('features_inter.csv')

df2 = pd.DataFrame(np.column_stack([indexes, allDists]), 
                  columns=['comparacao','distancia']).to_csv('all_dist.csv')
