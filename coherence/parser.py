import os
import pandas
import re
import unicodedata

files = os.listdir('/Users/andre/Documents/LegGo/Proposicoes/textos_publicados')
#import pdb;pdb.set_trace()
for f in files:
    if f != '.DS_Store':
        with open('textos_publicados/'+f, 'r', encoding='UTF8') as doc:
            text = doc.read().replace('\n', ' ')
            phrases = []
            texto = ""
            arts = text.split('Art.')
            for art in arts:
                paragraphs = art.split('§')
                for paragraph in paragraphs:            
                    incisos = re.split(r'[MDCLXVI]+\ -', paragraph, flags=re.IGNORECASE)
                    if len(incisos) == 1:
                        #import pdb;pdb.set_trace()
                        phrases.append(paragraph)
                    else:
                        for inciso in incisos[1:]:
                            texto += incisos[0] + " "                
                            alineas = re.split(r'(1. –)\)', inciso, flags=re.IGNORECASE)
                            #import pdb;pdb.set_trace()
                            if len(alineas)== 1:
                                texto += inciso + " "
                                phrases.append(texto)
                                texto = ""
                            else:
                                texto += alineas[0] + " "
                                for alinea in alineas[1:]:
                                    texto += alinea + " "
                                #import pdb;pdb.set_trace()
                                phrases.append(texto)
                                texto = ""
        new_phrases = []
        for p in phrases:
            new_phrases.append(unicodedata.normalize("NFKD", p))
        with open('textos_convertidos/'+f,'w', encoding='UTF8') as doc:
            for p in new_phrases:
                doc.write(p + '\n')
