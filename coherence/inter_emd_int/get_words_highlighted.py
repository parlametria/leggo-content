
# coding: utf-8

# In[8]:

import os
from gensim.models import KeyedVectors
import numpy as np
import math
import sys
from pathlib import Path
from collections import defaultdict
from aux import *

# In[9]:

import pandas as pd

# In[10]:

# Argumentos que o programa deve receber:
# -1º: Path para pasta onde estão os textos extraídos
# -2º: Path para o arquivo .bin do modelo Word2Vec treinado
# -3º: wmdistance ou distance
# -4º: Path para o arquivo onde o txt das palavras destoantes será salvo

if len(sys.argv) < 5:
    print_usage("get_words_highlighted")
    exit(1)

filesPath = sys.argv[1]
modelPath = sys.argv[2]
modelFunction = sys.argv[3]
outputPath = sys.argv[4]

# =============================================================================
# Paths para teste
# filesPath = Path('../mpv870/teste')
# modelPath = Path('../languagemodel/vectors_skipgram_lei_aprovadas.bin')
# =============================================================================

files = os.listdir(filesPath)
files = [value for value in files if len(value.split('.DS_Store'))==1]
model = KeyedVectors.load_word2vec_format(modelPath, binary=True)

# # Intercoerência

# In[11]:
    
emdSentences = []
intFile = ""

for file in files:
    #Verifica se o texto é de uma emenda
    if "emenda" in str(file):
        emdSentences.append(tokanizer_files(filesPath, file))

    #Verifica se existe o texto inicial da materia
    elif "avulso_inicial_da_materia" in str(file) or "apresentacao_de_proposicao" in str(file):
        intFile, id_proposicao = get_avulso_inicial(filesPath, file, files)
    else:
        files.remove(file)

if len(emdSentences) == 0:
    print("Não existe Emendas para esta proposição")
    sys.exit() 

if intFile == "":
    print("Texto inicial da proposição não encontrado")
    sys.exit() 

intSentences = quebra_avulso_sentencas(intFile)

# In[12]:

indexes = []
files_read = []

distancesDict = defaultdict(list)
for emd, i in zip(emdSentences, files):
    emd = emd[0]
    prefixo_emenda = i.split('.txt')[0]
    files_read.append(prefixo_emenda)

    f= open(outputPath,"a+")
    print("abrindo emenda:", prefixo_emenda)
    f.write(str(prefixo_emenda) + "\n")
    
    min_teor_sentence = calcula_distancia(emd, intSentences, [], indexes, model, i)
    print(show_diff(' '.join(min_teor_sentence), ' '.join(emd)))

    distancesDict = palavras_destoantes(get_distance_func(modelFunction, model), min_teor_sentence, emd)
    
    f.write("Palavras da emenda: " + str(emd) + "\n")
    f.write("Palavras da linha do avulso com menor distância: " + str(min_teor_sentence) + "\n")
    max_distance = -1
    max_mean = -1
    max_median = -1
    max_key = ""
    max_mean_key = ""
    max_median_key = ""
    for key in distancesDict:
        distances = np.array(distancesDict[key])
        distancesDict[key] = distances

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

    f.write("Palavra mais distante do texto da proposição: " + str(max_key) + "\n")
    f.write("Palavra com maior média: " + str(max_mean_key) + "\n")
    f.write("Palavra com maior mediana: " + str(max_median_key) + "\n")
    f.write(("=======================================================\n"))
    f.close()
    distancesDict = defaultdict(list)
