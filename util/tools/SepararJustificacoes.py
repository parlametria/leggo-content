
# coding: utf-8

# # Programa para separar as justificações dos textos de lei em Projetos de Lei
# Assumindo como entrada em linha de comando o caminho/path da pasta contendo os textos de projetos de lei

import os
import re
import sys

def print_usage():
    print("Número errado de parâmetros,o certo é: SepararJustificacoes.py <caminho_pasta_com_emendas_e_avulsos> <caminho_pasta_escrita> <log_arquivos_sem_texto>")

#Retorna a proposição toda se não houver justificação ou
#da o split quando há justificação e retorna o texto completo
#ou quando não de match com nenhum padrão retorna uma string vazia
def getTextoPrincipal(patterns, pl, textosPat):
    for i in range(len(patterns)):
        if re.search(patterns[i], pl):
            if textosPat[i] == "":
                return (pl)
            else:
                return(re.split(textosPat[i], pl, maxsplit = 1, flags = re.IGNORECASE)[0])
    
    return ""

if len(sys.argv) < 4:
	print_usage()
else:
	
    dirPath = sys.argv[1]
    justificacoesPath = sys.argv[2]
    descartadosPath = sys.argv[3]

    # # Expressões regulares utilizadas

    pat = re.compile(r"\njustificação\n",flags = re.IGNORECASE)
    pat2 = re.compile(r"\njustificativa\n",flags = re.IGNORECASE)
    pat3 = re.compile(r"projeto de lei|emenda|avulso|inteiro teor|materia|substitutivo", flags = re.IGNORECASE)
    patterns = [pat, pat2, pat3]
    textosPat = [r"\njustificação\n", r"\njustificativa\n", ""]

    os.makedirs(justificacoesPath, exist_ok=True)

    fps = []

    for dirpath, dirnames, filenames in os.walk(dirPath):
        for filename in filenames:
                # Cria diretórios no formato /justificacoes/numProposicao/arquivos.txt
                newPath = justificacoesPath + "/" + filename.split("_")[1] + "/"
                os.makedirs(newPath, exist_ok=True)
                docPath = os.path.join(dirpath,filename)
                with open(os.path.normpath(docPath), "r", encoding = "utf-8") as pl:
                    ProjetoDeLei = pl.read()
                    textoPrincipal = getTextoPrincipal(patterns, ProjetoDeLei, textosPat)
                    if textoPrincipal != "":
                        with open(newPath + os.path.splitext(filename)[0] + '.txt', 'w',encoding = 'utf-8') as j:
                            j.write(textoPrincipal)
                    else:
                        print("Documento: " + str(docPath) + " não possui textos")
                        with open(descartadosPath, 'a', encoding = 'utf-8') as j:
                            j.write(docPath)

                    

                    
                    
