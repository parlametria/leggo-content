import re
from nltk.corpus import stopwords
from string import punctuation
import sys
from collections import defaultdict
import traceback
import gensim

stop_words = set(stopwords.words('portuguese') + list(punctuation) + ['art', 'arts', 'Art', 'Arts'])

def tokanizer_files(path, file):
    emdSentences = []
    file = open(path + '/' + str(file), 'r', encoding = 'UTF8')
    line = file.read()
    line = " ".join(gensim.utils.simple_preprocess(line))
    tokenized_sentences = []
    line = re.sub(r'[^\w\d\s]+', '', line)
    tokenized_sentences.append(line.lower().split())
    for t in tokenized_sentences:
        emdSentences.append([w for w in t if w not in stop_words]) 

    return (emdSentences) 

def get_avulso_inicial(path, file, files):
    intFile = open(path + '/' + str(file), 'r', encoding = 'UTF8') 
    id_proposicao = str(file).split('_')[1]
    print("ID Proposição: " + id_proposicao)
    files.remove(file)

    return ([intFile, id_proposicao])

def quebra_avulso_sentencas(file_avulso_inicial):
    intSentences = []
    sub = re.split("(\r\n|\r|\n|“)+art|(\r\n|\r|\n)+§", str(file_avulso_inicial.read()), flags=re.IGNORECASE)
    for line in sub:
        if (line != None and line.strip() != ""):
            tokenized_sentences = []
            line = str(line)
            line = " ".join(gensim.utils.simple_preprocess(line))
            line = re.sub(r'[^\w\d\s]+', '', line)
            tokenized_sentences.append(line.lower().split())
            for t in tokenized_sentences:
                intSentences.append([w for w in t if w not in stop_words])

    return([w for w in intSentences if len(w) != 0])

def calcula_distancia(emd, intSentences, distances, indexes, model, i):
    min_teor_sentence_dist = sys.maxsize
    min_teor_sentence = ""
    for teor,j in zip(intSentences,range(len(intSentences))):
        if len(emd) > 4 and len(teor) > 4:
            d = model.wmdistance(emd,teor)
            if float("inf") == d:
                continue
            if (d < min_teor_sentence_dist):
                min_teor_sentence_dist = d
                min_teor_sentence = teor

            # Distância para calcular a média
            distances.append(d)
            # dists é uma lista de todas as distâncias calculadas
            indexes.append('_'.join([i, str(j)]))
    return(min_teor_sentence)

def palavras_destoantes(function, min_teor_sentence, emd, show_error_msg = False):
    distancesDict = defaultdict(list)
    for teorWord in min_teor_sentence:
        for emdWord in emd:
            try:
                d = function(emdWord, teorWord)
                if float("inf") == d:
                    continue

                distancesDict[emdWord].append(d)
            except Exception:
                if show_error_msg:
                    print(traceback.print_exc())
                continue
    return distancesDict

def get_distance_func(function, model):
    if (function == "wmdistance"):
        return model.wmdistance
    else:
        return model.distance

def print_usage(function_name):
    if function_name == "get_words_highlighted":
        print ("Chamada Correta: python3 get_words_highlighted.py <filesPath> <modelPath> <modelFunction> <outputPath>")
    elif function_name == "inter_emd_int":
        print ("Chamada Correta: python3 inter_emd_int.py <filesPath> <modelPath> <outputPath>")
    else:
        print ("Nome de função não reconhecido!")
