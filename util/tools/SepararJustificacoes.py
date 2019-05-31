
# coding: utf-8

# # Programa para separar as justificações dos textos de lei em Projetos de Lei
# Assumindo como entrada em linha de comando o caminho/path da pasta contendo os textos de projetos de lei

import os
import re
import sys

if len(sys.argv) > 3:
	print("Número de argumentos maior que um, insira somente o path para a pasta onde estão as PLs")
	
dirPath = sys.argv[1]
justificacoesPath = sys.argv[2]

# # Expressões regulares utilizadas

pat = re.compile(r"\njustificação\n",flags = re.IGNORECASE)
pat2 = re.compile(r"\njustificativa\n",flags = re.IGNORECASE)

# # Cria diretrio se não existe
def createDirsIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)

#dirPath = "./pls_leis_tramitacoes/textos_iniciais_txt"
#justificacoesPath = "./justificacoes/"
createDirsIfNotExists(justificacoesPath)

fps = []

for dirpath, dirnames, filenames in os.walk(dirPath):
    for filename in filenames:
            # Cria diretórios no formato /justificacoes/numProposicao/arquivos.txt
            newPath = justificacoesPath + "/" + filename.split("_")[1] + "/"
            createDirsIfNotExists(newPath)
        
            with open(os.path.normpath(os.path.join(dirpath,filename)), 'r', encoding = 'utf-8') as pl:
                ProjetoDeLei = pl.read()
            
                if re.search(pat,ProjetoDeLei):
                    justificacao = re.split(r"\njustificação\n", ProjetoDeLei, maxsplit = 1, flags = re.IGNORECASE)[0]
                
                    with open(newPath + os.path.splitext(filename)[0] + '_emenda.txt', 'w',encoding = 'utf-8') as j:
                        j.write(justificacao)

                if re.search(pat2,ProjetoDeLei):
                    justificacao = re.split(r"\njustificativa\n", ProjetoDeLei, maxsplit = 1, flags = re.IGNORECASE)[0]
                
                    with open(newPath + os.path.splitext(filename)[0] + '_emenda.txt', 'w',encoding = 'utf-8') as j:
                        j.write(justificacao)
                    
                    
