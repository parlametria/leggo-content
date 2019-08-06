
# coding: utf-8

# In[8]:

import os
from gensim.models import KeyedVectors
import numpy as np
import math
import sys
from pathlib import Path
from aux import *

# In[9]:

import pandas as pd

# In[10]:

# Argumentos que o programa deve receber:
# -1º: Path para pasta onde estão os textos extraídos
# -2º: Path para o arquivo .bin do modelo Word2Vec treinado 
# -3º: Path para a pasta onde a tabela de features deve ser salva

if len(sys.argv) < 4:
    print_usage("inter_emd_int")
    exit(1)

filesPath = sys.argv[1]
modelPath = sys.argv[2]
outputPath = sys.argv[3]

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

# Lista de Sentenças de cada emenda
    
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

means = []
variances=[]
stds = []
sqdmeans = []
totdists = []

allDists = []
indexes = []
files_read = []

for emd,i in zip(emdSentences,files):
    emd = emd[0]

    prefixo_emenda = i.split('.txt')[0]
    files_read.append(prefixo_emenda)

    print("abrindo emenda:",prefixo_emenda)
    distances = []
    
    calcula_distancia(emd, intSentences, distances, indexes, model, i)
            
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


#df = pd.DataFrame(np.column_stack([files_read, means, variances, stds, sqdmeans, totdists]), 
#	          columns=['files','mean_distance', 'variance', 'standard_deviation', 'sqd_means', 'total_distances']).to_csv(str(id_proposicao) + '_features_inter.csv')

prop_emendas_dists = pd.DataFrame(np.column_stack([indexes, allDists]), 
	          columns=['comparacao','distancia'])
prop_emendas_dists.index.name = 'index'
prop_emendas_dists.to_csv(str(outputPath) + str(id_proposicao) + '_all_dist.csv')
