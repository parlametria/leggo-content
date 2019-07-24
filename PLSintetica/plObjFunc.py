# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:02:36 2019

@author: lucas
"""
import re
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
            
            