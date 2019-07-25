
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

# In[9]:

import pandas as pd

# In[10]:

# Argumentos que o programa deve receber:
# -1º: Path para pasta onde estão os textos das emendas extraídas
# -2º: Path para o arquivo .bin do modelo Word2Vec treinado 
# -3º: Path para a pasta onde a tabela de features deve ser salva


emdPath = sys.argv[1]
modelPath = sys.argv[2]
outputPath = sys.argv[3]

# =============================================================================
# Paths para teste
# emdPath = Path('../mpv870/teste')
# modelPath = Path('../languagemodel/vectors_skipgram_lei_aprovadas.bin')
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
intFile = ""
for file in files:
    #Verifica se o texto é de uma emenda
    if "emenda" in str(file):
        file = open(emdPath + '/' + str(file), 'r', encoding = 'UTF8')
        line = file.read()
        tokenized_sentences = []
        line = re.sub(r'[^\w\d\s]+', '', line)
        tokenized_sentences.append(line.lower().split())
        stop_words = set(stopwords.words('portuguese') + list(punctuation))
        for t in tokenized_sentences:
            emdSentences.append([w for w in t if w not in stop_words])

    #Verifica se existe o texto inicial da materia
    elif "avulso_inicial_da_materia" in str(file) or "apresentacao_de_proposicao" in str(file):
        intFile = open(emdPath + '/' + str(file), 'r', encoding = 'UTF8') 
        id_proposicao = str(file).split('_')[1]
        print("ID Proposição: " + id_proposicao)
        files.remove(file)
    else:
        files.remove(file)

if len(emdSentences) == 0:
    print("Não existe Emendas para esta proposição")
    sys.exit() 
# =============================================================================
# lines = intFile.readlines()
# =============================================================================
if intFile == "":
    print("Texto inicial da proposição não encontrado")
    sys.exit() 

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

allDists = []
indexes = []
files_read = []

for emd,i in zip(emdSentences,files):
    prefixo_emenda = i.split('.txt')[0]
    files_read.append(prefixo_emenda)

    print("abrindo emenda:",prefixo_emenda)
    distances = []
    max_distance = 99999999
    max_emd = ''
    max_teor = ''
    
    for teor,j in zip(intSentences,range(len(intSentences))):
        
        if len(emd) > 4 and len(teor)> 4:
            d = model.wmdistance(emd,teor)
            if float("inf") == d:
                continue

            if d <= max_distance:
                max_distance = d
                max_emd = emd
                max_teor = teor

            # Distância para calcular a média
            distances.append(d)
            # dists é uma lista de todas as distâncias calculadas
            indexes.append('_'.join([i, str(j)]))
            
    distances = np.array(distances) 

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

allDists = np.array(allDists)

indexes = np.array(indexes)

def word2vec(word):
    from collections import Counter
    from math import sqrt

    cw = Counter(word)
    sw = set(cw)
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    common = v1[1].intersection(v2[1])
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]

wordtuples = []
for key in max_teor:
    for word in max_emd:
        try:
            res = cosdis(word2vec(word), word2vec(key))
            print("The cosine similarity between : {} and : {} is: {}".format(word, key, res*100))
            wordtuples.append((word, key, res*100))
        except IndexError:
            pass
wordtuples.sort(key = lambda element: element[2], reverse=True)
for i in wordtuples:
    print(i, )

#df = pd.DataFrame(np.column_stack([files_read, means, variances, stds, sqdmeans, totdists]), 
#	          columns=['files','mean_distance', 'variance', 'standard_deviation', 'sqd_means', 'total_distances']).to_csv(str(id_proposicao) + '_features_inter.csv')

prop_emendas_dists = pd.DataFrame(np.column_stack([indexes, allDists]), 
	          columns=['comparacao','distancia'])
prop_emendas_dists.index.name = 'index'
prop_emendas_dists.to_csv(str(outputPath) + str(id_proposicao) + '_all_dist.csv')

