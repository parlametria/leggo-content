
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
from collections import defaultdict
import traceback

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

files = [value for value in files if len(value.split('.DS_Store')) == 1]

means = []
variances = []
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
    # Verifica se o texto é de uma emenda
    if "emenda" in str(file):
        file = open(emdPath + '/' + str(file), 'r', encoding='UTF8')
        line = file.read()
        tokenized_sentences = []
        line = re.sub(r'[^\w\d\s]+', '', line)
        tokenized_sentences.append(line.lower().split())
        stop_words = set(stopwords.words('portuguese') + list(punctuation) + ['art', 'arts', 'nº', 'nr'])
        for t in tokenized_sentences:
            emdSentences.append([w for w in t if w not in stop_words])

    # Verifica se existe o texto inicial da materia
    elif "avulso_inicial_da_materia" in str(file) or "apresentacao_de_proposicao" in str(file):
        intFile = open(emdPath + '/' + str(file), 'r', encoding='UTF8')
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


sub = re.split("(\r\n|\r|\n|“)+Art|(\r\n|\r|\n)+§",  str(intFile.read()), flags=re.IGNORECASE)
for line in sub:
    if (line != None and line.strip() != ""):
        tokenized_sentences = []
        line = str(line)
        line = re.sub(r'[^\w\d\s]+', '', line)
        
        tokenized_sentences.append(line.lower().split())
        stop_words = set(stopwords.words('portuguese') + list(punctuation))
        for t in tokenized_sentences:
            intSentences.append([w for w in t if w not in stop_words])

intSentences = [w for w in intSentences if len(w) != 0]

# # In[12]:

means = []
variances = []
stds = []
sqdmeans = []
totdists = []

allDists = []
indexes = []
files_read = []

distancesDict = defaultdict(list)
for emd, i in zip(emdSentences, files):
    prefixo_emenda = i.split('.txt')[0]
    files_read.append(prefixo_emenda)

    f= open("distance.txt","a+")
    print("abrindo emenda:", prefixo_emenda)
    f.write(str(prefixo_emenda) + "\n")
    
    min_teor_sentence_dist = 99999999999999
    min_teor_sentence = ""
    for teor, j in zip(intSentences, range(len(intSentences))):
        if len(emd) > 4 and len(teor)> 4:
            d = model.wmdistance(emd,teor)
            if float("inf") == d:
                continue
            if (d < min_teor_sentence_dist):
                min_teor_sentence_dist = d
                min_teor_sentence = teor


    for teorWord in min_teor_sentence:
        for emdWord in emd:
            try:
                d = model.distance(emdWord, teorWord)
                if float("inf") == d:
                    continue

                # dists é uma lista de todas as distâncias calculadas
                indexes.append('_'.join([i, str(j)]))
                distancesDict[emdWord].append(d)
            except Exception:
                continue
    #print(distancesDict.keys())
    
    f.write(str(emd) + "\n")
    f.write("Linha do avulso com menor distância: " + str(min_teor_sentence) + "\n")
    f.write(str(distancesDict.keys()) + "\n")
    max_distance = -1
    max_mean = -1
    max_median = -1
    for key in distancesDict:
        distances = np.array(distancesDict[key])
        distancesDict[key] = distances

        allDists.extend(distances)
        soma = distances.sum()
        if(soma > max_distance):
            max_distance = soma
            max_key = key
        mean = distances.mean()
        if(mean > max_mean):
            max_mean = mean
            max_mean_key = key
        median = np.median(distances)
        if(median > max_median):
            max_median = median
            max_median_key = key
        var = distances.var()
        std = math.sqrt(distances.var())
        totdist = distances.sum()

        # f.write(("=======================================================\n"))
        #f.write(str(key) + "\n")
        #f.write("Soma: " + str(soma) + "\n")
        #f.write("Média: " + str(mean) + "\n")
        #f.write("Mediana: " + str(median) + "\n")
        #f.write("Variação: " + str(var) + "\n")
        #f.write("Desvio padrão: " + str(std) + "\n")
        means.append(mean)
        variances.append(var)
        stds.append(std)
        totdists.append(totdist)
    f.write("Palavra mais distante do texto da proposição: " + str(max_key) + "\n")
    f.write("Palavra com maior média: " + str(max_mean_key) + "\n")
    f.write("Palavra com maior mediana: " + str(max_median_key) + "\n")
    f.write(("=======================================================\n"))
    f.close()
    distancesDict = defaultdict(list)

# allDists = np.array(allDists)

# indexes = np.array(indexes)


# def word2vec(word):
#     from collections import Counter
#     from math import sqrt

#     cw = Counter(word)
#     sw = set(cw)
#     lw = sqrt(sum(c*c for c in cw.values()))

#     # return a tuple
#     return cw, sw, lw


# def cosdis(v1, v2):
#     common = v1[1].intersection(v2[1])
#     return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]


# wordtuples = []
# for key in max_teor:
#   for word in max_emd:
#      try:
#         res = cosdis(word2vec(word), word2vec(key))
#        print("The cosine similarity between : {} and : {} is: {}".format(word, key, res*100))
#       wordtuples.append((word, key, res*100))
#  except IndexError:
#     pass
#wordtuples.sort(key = lambda element: element[2], reverse=True)
# print(max_emd)
# print(max_teor)
# for i in wordtuples:
#    print(i, )

# df = pd.DataFrame(np.column_stack([files_read, means, variances, stds, sqdmeans, totdists]),
#	          columns=['files','mean_distance', 'variance', 'standard_deviation', 'sqd_means', 'total_distances']).to_csv(str(id_proposicao) + '_features_inter.csv')

# prop_emendas_dists = pd.DataFrame(np.column_stack([indexes, allDists]),
#                                   columns=['comparacao', 'distancia'])
# prop_emendas_dists.index.name = 'index'
# prop_emendas_dists.to_csv(
#     str(outputPath) + str(id_proposicao) + '_all_dist.csv')
