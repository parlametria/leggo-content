
# coding: utf-8

# # Programa para separar as justificações dos textos de lei em Projetos de Lei
# Assumindo como entrada em linha de comando o caminho/path da pasta contendo os textos de projetos de lei


import os
import re
import sys



if len(sys.argv) > 2:
	print("Número de argumentos maior que um, insira somente o path para a pasta onde estão as PLs")
	
dir_path = sys.argv[1]

# # Expressões regulares utilizadas

pat = re.compile(r"\njustificação\n",flags = re.IGNORECASE)

# # Cria pasta com as justificações

os.mkdir('justificacoes')

dirPath = sys.argv[1]

#dirPath = "./pls_leis_tramitacoes/textos_iniciais_txt"

fps = []

for dirpath, dirnames, filenames in os.walk(dirPath):
    for filename in filenames:
        
        with open(os.path.normpath(os.path.join(dirpath,filename)), 'r', encoding = 'utf-8') as pl:
            ProjetoDeLei = pl.read()
            
            if re.search(pat,ProjetoDeLei):
                justificacao = re.split(r"\njustificação\n", ProjetoDeLei, maxsplit = 1, flags = re.IGNORECASE)[1]
                
                with open("./justificacoes/" + os.path.splitext(filename)[0] + '_jus.txt', 'w',encoding = 'utf-8') as j:
                    j.write(justificacao)
                    