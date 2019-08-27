# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:02:36 2019

@author: lucas
"""
import re
import string

def PlObjCreate(path):
    
    
# Listas de Artigos, Listas de Parágrafos, listas de incisos, listas de alineas
    PlObj = []
    PlArt = []
    PlPar = []
    PlInc = []
    PlAli = []
    
    # Regex para encontrar níveis no texto
    
    artPat = re.compile(r'\nArt\. \dº. +|\nArt\. \d+. +')
    parPat = re.compile(r'\n§ \d+º|\nParágrafo único\.')
    incPat = re.compile(r'\n[MDCLXVI]+\ - +')
    aliPat = re.compile(r'\n[a-z]\)|\n[a-z][a-z]\)')
    
    
    with open (path, 'r', encoding = 'utf-8') as pl:
        texto = pl.read()
        
        arts = re.split(artPat,texto)
        for art in arts:
            if arts.index(art) == 0:
                # Acrescenta o texto anterior ao 1º artigo a lista PlObj
                PlObj.append(art)
                PlArt.append("")
                continue   
            paragraphs = re.split(parPat,art)
            
            # Caso o próximo nível seja de parágrafo
            if len(paragraphs)>1:
                for paragraph in paragraphs:
                    par = []
                    par.append(re.match(r'.+\b',paragraph.strip())[0])
                    
                    
                    incisos = re.split(incPat,paragraph)
                    if len(incisos) > 1:
                        for inciso in incisos: 
                            if incisos.index(inciso) == 0:
                                PlInc.append('')
                                inc = []
                                continue
                            
                            inc.append(re.match(r'.+\b',inciso.strip())[0])
                            
                            alineas = re.split(aliPat,inciso)
                            if len(alineas) > 1:
                                for alinea in alineas:
                                    if alineas.index(alinea) == 0:
                                        PlAli.append("")
                                        continue
                                    PlAli.append(re.match(r'.+\b',alinea.strip())[0])                   
                                    
                            inc.append(PlAli)
                            PlInc.append(inc)
                            inc = []
                            PlAli = []
                            
                    par.append(PlInc)
                    PlPar.append(par)
                    PlInc = []
                    
                PlArt.append(PlPar)
                PlPar = []
                continue
            
            # Caso o próximo nível seja de inciso
            par = []
            incisos = re.split(incPat,art)
            if len(incisos) > 1:
                for inciso in incisos:
                    if incisos.index(inciso) == 0:
                        par.append(re.match(r'.+\b',inciso.strip())[0])
                        PlInc.append('')
                        inc = []
                        continue
                    inc.append(re.match(r'.+\b',inciso.strip())[0])
                    
                    alineas = re.split(aliPat,inciso)
                    if len(alineas) > 1:
                        for alinea in alineas:
                            if alineas.index(alinea) == 0:
                                PlAli.append('')
                                continue
                            PlAli.append(re.match(r'.+\b',alinea.strip())[0])
                            
                    inc.append(PlAli)
                    PlInc.append(inc)
                    inc = []
                    PlAli = []
                    
                par.append(PlInc)
                PlPar.append(par)
                PlInc = []
                PlArt.append(PlPar)
                PlPar = []
                
            else:
                par = []
                par.append(re.match(r'.+\b',art.strip())[0])
                PlPar.append(par)
                PlArt.append(PlPar)
                par = []
                PlPar = []
                
        PlObj.append(PlArt)
    return(PlObj)
            
def num_to_ali(nr):
    letra = ''
    if float(nr/25) > 1:
        for i in range(nr//25):
            letra += string.ascii_lowercase[i]
    letra += string.ascii_lowercase[(nr%26)]
    return letra
    
def int_to_roman(input):
    if not isinstance(input, type(1)):
        raise (TypeError, "expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise (ValueError, "Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

def pl_to_txt(plobj):
    with open("obj_out.txt", mode = 'w', encoding = "utf8") as pl_txt:
        for i, titulo in enumerate(plobj):
            if type(titulo) == str:
                pl_txt.write(titulo)
            else:
                for j, lista_de_paragrafos in enumerate(titulo):
                    if j == 0:
                        pass
                    else:
                        for k, sublista in enumerate(lista_de_paragrafos):
                            for m, paragrafo in enumerate(sublista):
                                if type(paragrafo) == str:
                                    if k == 0:
                                        pl_txt.write('\nArt. {} {}\n'.format(j,paragrafo))                            
                                    else:
                                        pl_txt.write('\n§{}'.format(k) + paragrafo + '\n')
                                else:
                                    for n, lista_de_inciso in enumerate(paragrafo):
                                        if n == 0:
                                            pass
                                        else:
                                            for o, inciso in enumerate(lista_de_inciso):
                                                if type(inciso) == str:
                                                    pl_txt.write('\n{} - '.format(int_to_roman(n)) + inciso + '\n')
                                                else:
                                                    for l, lista_de_alinea in enumerate(inciso):
                                                        if l == 0:
                                                            pass
                                                        else:
                                                            pl_txt.write('\n{}) '.format(num_to_ali(l-1)) + lista_de_alinea + '\n')
            








            