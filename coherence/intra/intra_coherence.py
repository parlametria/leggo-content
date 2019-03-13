
# coding: utf-8

# In[8]:


from time import time
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
from sklearn.preprocessing import normalize


# In[10]:

# Argumentos que o programa deve receber:
# -1º: Path para pasta onde estão os textos/PLs extraídas
# -2º: Path para o arquivo .bin do modelo Word2Vec treinado 
# -3º: Path para a pasta onde a tabela de features deve ser salva

#files = os.listdir('C:/Users/lucas/Documents/UFMG/Projeto/coherence/leggo-content/coherence/mpv870/teste') # mudar path para pasta das justificações 
filesPath = Path(sys.argv[1])
modelPath = Path(sys.argv[2])
outputPath = Path(sys.argv[3])

files = os.listdir(filesPath)

files = [value for value in files if len(value.split('txtlog'))==1]

means = []
variances=[]
stds = []
sqdmeans = []
totdists = []
model = KeyedVectors.load_word2vec_format(modelPath, binary=True)


# # Intracoerência

# In[ ]:
if not Path(outputPath/'features_intra').exists():
    os.mkdir(outputPath / 'features_intra')

num = 3199
for file in files:
    dirname = file.split('.txt')[0]
    if not Path(outputPath/'features_intra' / dirname).exists():
        os.mkdir(Path(outputPath/'features_intra'/dirname))    
        
        print(f'Calculating features for {dirname} number {num}')
        file = open(filesPath/file, 'r', encoding = 'UTF8')
        
        lines = file.readlines()
        tokenized_sentences = []
        
        for line in lines:
            line = re.sub(r'[^\w\d\s]+', '', line)
            tokenized_sentences.append(line.lower().split())

        stop_words = set(stopwords.words('portuguese') + list(punctuation))
        final_tokenized_sentences= []

        for t in tokenized_sentences:
            final_tokenized_sentences.append([w for w in t if w not in stop_words])

        distances = []
        indexes =[]
        
        for i in range(0,len(final_tokenized_sentences)):  #ignora a primeira linha pois ignora "presidente da republica..."
            if i % 1 == 0:
                print(i)
                
            j = i
            for j in range(len(final_tokenized_sentences)): # ignora a linha da casa e data
                if len(final_tokenized_sentences[i] ) > 4 and len(final_tokenized_sentences[j] )> 4:
                    distances.append(model.wmdistance(final_tokenized_sentences[i], final_tokenized_sentences[j]))
                    indexes.append((i, j))
        distances = np.array(distances)
        distances = distances/np.sqrt((distances**2).sum())
        
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
        

        np.savetxt(os.path.join(outputPath,'features_intra', dirname,"distances.csv"),distances.astype(float), fmt='%f', delimiter=",")
        new_indexes = np.asarray(indexes)
        np.savetxt(os.path.join(outputPath,'features_intra',dirname,"indexes.csv"), new_indexes.astype(int), fmt='%i',delimiter=',')
        num-=1
    else:
        print(filesPath.name + 'features_intra' + dirname + ' number ' +str(num) +  ' already exists')
        num-=1
        
df = pd.DataFrame(np.column_stack([files, means, variances, stds, sqdmeans, totdists]), 
                               columns=['files','mean_distance', 'variance', 'standard_deviation', 'sqd_means', 'total_distances']).to_csv(outputPath/'features.csv')
    


