import os
import pandas
import re
import unicodedata

files = os.listdir('/Users/andre/Documents/LegGo/Proposicoes/textos_iniciais_convertidos')
#import pdb;pdb.set_trace()
for f in files:
    with open('textos_iniciais_convertidos/'+f,'r', encoding='UTF8') as doc:
        final = open('textos_sem_espaco_finais/'+f, 'w', encoding='UTF8')
        phrases = doc.readlines()
       
        for ps in phrases:           
            final.write(re.sub(' +', ' ', ps))
        
        final.close()