import os
import pandas
import re
import unicodedata
files = os.listdir('/Users/andre/Documents/LegGo/Proposicoes/textos_convertidos')
#import pdb;pdb.set_trace()
for f in files:
    with open('textos_convertidos/'+f,'r', encoding='UTF8') as doc:
        final = open('textos_iniciais_convertidos/'+f, 'w', encoding='UTF8')
        #log = open('textos_iniciais_convertidos/'+f+'log.txt', 'w', encoding='UTF8')
        phrases = doc.readlines()
        for ps in phrases:
            #import pdb;pdb.set_trace()
            if re.search(r'([0-9]o )|([0-9]*. )|([0-9]*:)|([0-9].[0-9]* )', ps) != None:
                #log.write(ps[: re.search(r'([0-9]o )|([0-9]*. )|([0-9]*:)|([0-9].[0-9]* )', ps).end()])
                final.write(ps[: re.search(r'([0-9]o )|([0-9]*. )|([0-9]*:)|([0-9].[0-9]* )', ps).start()] + ' '+ ps[re.search(r'([0-9]o )|([0-9]*. )|([0-9]*:)|([0-9].[0-9]* )', ps).end():])
                a = 0
        final.close()