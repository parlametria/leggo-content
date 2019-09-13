# -*- coding: utf-8 -*-

import re
import os
import sys
from unidecode import unidecode
import pandas as pd
import nltk
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import CountVectorizer
import ClassificadorDeEmendas as clfe
import plObjFunc as pl


def proc_agreg_out(agr_out):
    bet_quote = re.compile(r"\'(.*?)\'", flags=re.IGNORECASE)
    existe_agreg = False
    if re.search('__INICIO_AGREGADOR__', emd):
        nxt = emd.split("__INICIO_AGREGADOR__\n")[1]
        if re.search(r'.+\n(?=__FIM_AGREGADOR__)', nxt):
            ent = nxt.split('__FIM_AGREGADOR__')[0]
            existe_agreg = True

    lista_indices = []
    if existe_agreg:
        for item in ent.splitlines():
            item = re.findall(bet_quote, item)
            pl_index = []

            # Le todos os casos, cria uma lista com os indices para o obj pl
            for nr, index in enumerate(item):
                try:
                    if nr == 0 or nr == 1:
                        pl_index.append(int(index.split('_')[1]))
                    if nr == 2:
                        pl_index.append(pl.roman_to_int(index.split('_')[1]))
                    if nr == 3:
                        pl_index.append(pl.ali_to_num(index.split('_')[1]))
                except:
                    pl_index.append(None)

            # Tratamento de casos especiais
            # Desconsidera caso não exista artigo
            if not pl_index[0]:
                continue
            # Caso receba somente artigo e não parágrafo, use o
            # parágrafo 0
            if pl_index[0] and not pl_index[1] and pl_index[2]:
                pl_index[1] = 0
            # Caso receba somente artigo e alinea
            if (pl_index[0] and not pl_index[1] and not pl_index[3] and
                    pl_index[3]):
                pl_index[1] = 0
                pl_index[2] = 1

            # Retira valores None e inserir indices para correta localização
            pl_index = [i for i in pl_index if i is not None]
            if len(pl_index) == 4:
                pl_index.insert(2, 1)
                pl_index.insert(-1, 1)
            if len(pl_index) == 3:
                pl_index.insert(-1, 1)

            lista_indices.append(pl_index)
    return lista_indices

# =============================================================================
# mpv = pl.PlObjCreate('./teste/mpv870/MPV870_txt_site.txt')
# emd_dir_path = '../parser_itens/emd_pars_agreg'
# modelPath = '../coherence/languagemodel/vectors_new.bin'
# =============================================================================


# Caminho para o arquivo .txt do inteiro teor
mpv = pl.PlObjCreate(sys.argv[1])
# Caminho para a pasta contendo as emendas tratadas pelo agregador
emd_dir_path = sys.argv[2]
# Caminho para o modelo .bin treinado do Skipgram
modelPath = sys.argv[3]

stp_wrd = nltk.download('stopwords')
tokenizer = CountVectorizer(stop_words=stp_wrd).build_tokenizer()
model = KeyedVectors.load_word2vec_format(modelPath, binary=True)

files = []
for dirpath, dirnames, filenames in os.walk(emd_dir_path):
    for filename in filenames:
        files.append(os.path.normpath(os.path.join(dirpath, filename)))

tipos_de_emenda = clfe.preve_emenda(emd_dir_path)

to_df_row = []
for file, tipo_emenda in zip(files, tipos_de_emenda):
    # Checa o tipo de emenda
    if tipo_emenda == 'O':
        continue

    with open(file, mode='r', encoding='utf8') as emenda:
        lista_de_itens_alterados = []

        emd = emenda.read()
        texto_emd = tokenizer(unidecode(emd.split("!@#$%")[0].lower()))

        # Processa emendas pós agregador

        lista_de_itens_alterados = proc_agreg_out(emd)

        for alteracao in lista_de_itens_alterados:
            if tipo_emenda == 'MOD':
                    # Procura posição no plObj
                    try:
                        texto_pl = pl.nested_lookup(mpv[1], alteracao)

                        # Cria uma string inteira com todos os textos na
                        # posição encontrada
                        texto_pl = ' '.join(list(pl.flatten(texto_pl))).lower()
                        texto_pl = tokenizer(unidecode(texto_pl))

                        alteracao = [str(i) for i in alteracao]
                        dist = model.wmdistance(texto_pl, texto_emd)
                        to_df_row.append([file, ' '.join(str(alteracao)), dist])

                    except IndexError:
                        alteracao = [str(i) for i in alteracao]
                        print("Elemento não encontrado {}, {}".format(file,
                              alteracao))

df = pd.DataFrame(to_df_row, index=True, columns=['file', 'item', 'dist'])
df.to_csv('df_csv.csv')
