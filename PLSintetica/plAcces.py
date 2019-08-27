# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 18:28:06 2019

@author: lucas
"""

import plObjFunc as pl

mpv = pl.PlObjCreate('./teste/mpv870/MPV870_txt_site.txt')

###
artigo = input()
paragrafo = input()
inciso = input()
alinea = input()

lista_in = []
for i in artigo, paragrafo, inciso, alinea:
    try:
        lista_in.append(int(i))
    except:
        lista_in.append(None)
###
        
        
with open("../parser_itens/testes_lucas/7909406.pdf_teor.tags",
          encoding = "utf8", 'r') as emenda:
    entidades = emenda.read().split("!@#$%")[1]
    
           
        
        


# =============================================================================
# try:
#     map()
# for i in niveis:
# =============================================================================
    
if artigo and paragrafo and inciso and alinea:
    try:
        print(mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][1][lista_in[3]])
    except:
        print("não existe, caso1")

if artigo and paragrafo and inciso and not alinea:
    try:
        print(mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][0])
    except:
        print("não existe")
        
if artigo and paragrafo and not inciso and not alinea:
    try:
        print(mpv[1][lista_in[0]][lista_in[2]])
    except:
        print("não existe")
        
texto_ADD = "texto adicionado"
texto_MOD = "texto_mod"

tipo_emenda = "SUP"

# teste: adicionar texto ao artigo 5 paragrafo 0 inciso 1

if tipo_emenda == "ADD":
    # não é necessário considerar a posição da alínea para inserir ela
        
    if artigo and paragrafo and inciso and not alinea:
        mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][1].append(texto_ADD)
        print(mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][1])
        
    if artigo and paragrafo and not inciso and not alinea:
        mpv[1][lista_in[0]][lista_in[1]].append(texto_ADD)
        print(mpv[1][lista_in[0]][lista_in[1]])
    
    if artigo and not paragrafo and inciso and not alinea:
        mpv[1][lista_in[0]][0][1][lista_in[2]].append(texto_ADD)
    
if tipo_emenda == "MOD":
    if artigo and paragrafo and inciso and alinea:
        mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][1][lista_in[3]] = texto_MOD
        print(mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][1][lista_in[3]])
        
    if artigo and paragrafo and inciso and not alinea:
        mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][0] = texto_MOD
        
    if artigo and paragrafo and not inciso and not alinea:
        mpv[1][lista_in[0]][lista_in[1]][0]  = texto_MOD
    
if tipo_emenda == "SUP":
    if artigo and paragrafo and inciso and alinea:
        mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][1][lista_in[3]] = ''
        
    if artigo and paragrafo and inciso and not alinea:
        mpv[1][lista_in[0]][lista_in[1]][1][lista_in[2]][0] = ''
        
    if artigo and paragrafo and not inciso and not alinea:
        mpv[1][lista_in[0]][lista_in[1]][0]  = ''

    
    