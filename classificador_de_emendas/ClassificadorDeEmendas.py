# -*- coding: utf-8 -*-

import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.pipeline import Pipeline
from joblib import dump, load

def cria_df_treino(ner_out_path):
    """ 
    A funcao cria um DataFrame pandas para posteriormente treinar o modelo
    função deve receber o caminho para uma pasta contendo os arquivos de
    saída do segmentador (tag files)
    """
    tagList = ['I-', 'E-', 'B-']
    files = []
    for dirpath, dirnames, filenames in os.walk(ner_out_path):
        for filename in filenames:
            files.append(os.path.normpath(os.path.join(dirpath, filename)))

    emendas = pd.DataFrame(columns = ['text', 'emdType'])
    tupEmd = []

    for file in files:
        with open(file, encoding = 'utf-8') as f:
            emdTxt = []
            previousType = None
            for line in f.readlines():
                token, emdType = line.split()
                if any(x in emdType for x in tagList):
                    emdType = emdType[2:]
                if previousType != emdType and previousType != None:
                    tupEmd.append([' '.join(emdTxt), previousType])
                    emdTxt = []
                
                emdTxt.append(token)
                previousType = emdType
            tupEmd.append([' '.join(emdTxt), emdType])

    for index in range(len(tupEmd)):
        emendas.loc[index, 'text'] = tupEmd[index][0]
        emendas.loc[index, 'emdType'] = tupEmd[index][1]
    return emendas

    
def cria_modelo(dataframe):
    """
    O modelo é criado a partir do DataFrame definido anteriormente.
    Utiliza como entrada um bag-of-words, um vetor que contem o numero 
    de ocorrencias de cada palavra em todas as emendas. A funcao tambem
    gera um arquivo pipeline do Scikit Learn para posterior uso em predicao
    """
    
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(dataframe['text'])
    y = dataframe['emdType']
    
    # Separacao das bases
    X_train, X_test, y_train, y_test = train_test_split( 
            X, y, test_size=0.33, random_state=42)
    
    # Oversampling e realizado pois ha poucas ocorrencias de emendas ADD
    ros = RandomOverSampler(random_state=0)
    X_resampled, y_resampled = ros.fit_resample(X, y)
    
    clf = SVC(gamma='auto', random_state=42)
    clf.fit(X_resampled,y_resampled)
    pipeline = Pipeline([('vectorizer', vectorizer), ('clf_emend', clf)])
    dump(pipeline, "emend_clf_pipe")
    return clf


def preve_emenda(path_emendas_em_blocos):
    """
    Função que cria as features a partir dos dados de saida do NER
    e retorna o tipo de emenda previsto.
    Utilize o caminho para a pasta da emenda segmentada em blocos
    """
    
    files = []
    for dirpath, dirnames, filenames in os.walk(path_emendas_em_blocos):
        for filename in filenames:
            files.append(os.path.normpath(os.path.join(dirpath, filename)))
    
    lista_de_emendas = []
    for file in files:
        with open(file, encoding = 'utf8') as emenda_txt:
            lista_de_emendas.append(emenda_txt.read())
        

    vec_clf = load('emend_clf_pipe')
    return vec_clf.predict(lista_de_emendas)
        
    
        
        