import string
import re
import os
import sys

def adicionaNoArquivo(arquivo, termo, enumerados):
        with open(arquivo, 'a') as arq:
                for enum in enumerados:
                        arq.write('\n' + termo + '_' + str(enum))

def comecaComTermo(termos_de_interesse, palavra):
        i = 0
        for termo in termos_de_interesse: #para cada palavra confere se é um termo de interesse
                if palavra.startswith(termo):
                        return [True, i] #se começa com um dos termos de interesse, retorna verdadeiro e a posição
                i += 1

        return [False, -1] #senão, retorna falso e uma posição inválida


def avaliaTerminacao(palavra, chars_de_terminacao):
        for char in chars_de_terminacao:
                if palavra.endswith(char) or palavra.endswith(' ' + char):
                        return True
        
        return False
        

def main():
        termos_de_interesse = ['art', 'alin', 'alín', 'inc', 'parag', 'parág', '§'] #utilizado para verificar 
        dicionario_termos = { #utilizado para substituição de termos depois
                0: 'artigo', 
                1: 'alinea', 
                2: 'alinea', 
                3: 'inciso', 
                4: 'paragrafo', 
                5: 'paragrafo',
                6: 'paragrafo'
        }
        algarismos_romanos = ['x', 'i', 'v', 'l', 'c', 'd', 'm']
        chars_de_terminacao = [':']

        pasta = os.listdir(sys.argv[1])

        for arqv in pasta:
                with open(sys.argv[1] + '/' + arqv, 'r') as arquivo:
                        texto = arquivo.read()

                with open(sys.argv[1] + '/' + arqv, 'a') as arquivo:
                        arquivo.write('\n\n!@#$%\n')


                texto = ' '.join(texto.lower().split()) #deixando apenas um espaço em branco
                texto = texto.replace('“ ', '“').replace(' ”', '”').replace("' ", "'").replace(" '", "'") #formatando as palavras para as alíneas sem alteração de sentido
                texto = texto.replace('‘ ', '‘').replace(' ’', '’').replace('" ', '"').replace(' "', '"')

                palavras = texto.split() #convertendo em lista de palavras
                print(palavras)

                i = 0
                while True: #caminha por todas as palavras da lista
                        if i == len(palavras) - 1:
                                break

                        comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                        if comeca_com_termo:
                                #se a palavra começa com um termo há duas opções: ou ela já possui um número/letra/algarismo romano de sua enumeração ou essa enumeração começa na próxima palavra. há a possibilidade de estar tudo junto, sem espaços. varre-se a palavra obtendo toda enumeração possível e, após o fim da palavra, continua a mesma procura nas próximas palavras até que se encontre uma palavra que possua um novo termo de interesse (ou até que o texto acabe).



                                #####################################################
                                # INÍCIO: avaliação no caso de Artigos e Parágrafos #
                                #####################################################
                                if posicao_na_lista in [0, 4, 5, 6]: #se estamos falando de parágrafo ou artigo então estamos buscando por números
                                        termo_atual = dicionario_termos[posicao_na_lista]
                                        numeros_na_enumeracao = [] #salva todos números da enumeração do termo atual

                                        numero = ''
                                        sem_append = True
                                        for char in palavras[i]: #obtém os números na palavra atual
                                                if char.isdigit():
                                                        numero += str(char)
                                                        sem_append = True
                                                else: #exemplo: "art.35,57", nesse caso obteremos os dois separadamente
                                                        if numero != '':
                                                                numeros_na_enumeracao.append(numero)
                                                                numero = ''
                                                                sem_append = False
                                        if sem_append and numero != '':
                                                numeros_na_enumeracao.append(numero)
                                        i += 1 #ao fim da avaliação da palavra atual passa para a próxima (até que se encontre um novo termo de interesse ou o fim do texto). essa redundância com o primeiro loop é devido ao fato de que alguns termos enumerem com números, outros com letras e outros com algarismos romanos. mantendo o controle da busca dentro da condição a avaliação fica mais simples.
                                        comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                                        contador_sem_termo_interesse = 0
                                        while i < len(palavras) - 1 and not comeca_com_termo and contador_sem_termo_interesse < 3: #enquanto ainda for possivelmente um conteúdo da enumeração do termo atual
                                                if avaliaTerminacao(palavras[i], chars_de_terminacao): 
                                                        i += 1 #ao sair do while há um i -= 1
                                                        break
                                                        flag_terminacao = True
                                                        
                                                numero = ''
                                                sem_append = True
                                                for char in palavras[i]: #obtém os números na palavra atual
                                                        if char.isdigit():
                                                                numero += str(char)
                                                                sem_append = True
                                                        else: #exemplo: "art.35,57", nesse caso obteremos os dois separadamente
                                                                if numero != '':
                                                                        numeros_na_enumeracao.append(numero)
                                                                        numero = ''
                                                                        sem_append = False
                                                if sem_append and numero != '':
                                                        numeros_na_enumeracao.append(numero)
                                                elif sem_append and numero == '': #se não houve um append e a palavra atual não representa nada para ser enumerado
                                                        contador_sem_termo_interesse += 1 #adiciona 1 no controlador de termos sem enumeração
                                                i += 1
                                                comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                                        i -= 1 #pode ter saído do loop ou por ter acabado o texto ou por ter encontrado um novo termo
                                        print(numeros_na_enumeracao)
                                        adicionaNoArquivo(sys.argv[1] + '/' + arqv, termo_atual, numeros_na_enumeracao)
                                        pass
                                ##################################################
                                # FIM: avaliação no caso de Artigos e Parágrafos #
                                ##################################################



                                ########################################
                                # INÍCIO: avaliação no caso de Incisos #
                                ########################################
                                #só pode salvar o algarismo se for xivlcdm e for rodeado apenas por espaços ou pontuações.
		                #exemplo: peixe xiv,xeque mate -> o x do peixe não é romano porque é rodeado por não romanos ou espaço ou pontuação
                                elif posicao_na_lista in [3]: #algarismos romanos: xivlcdm
                                        termo_atual = dicionario_termos[posicao_na_lista]
                                        algarismos_na_enumeracao = [] #salva todos algarismos da enumeração do termo atual

                                        possiveis_romanos = re.split('\W+', palavras[i]) #separa a palavra por tudo aquilo que não é um não caractere de palavras
                                        for plv in possiveis_romanos:
                                                if all(c in "xivlcdm" for c in plv) and plv != '':
                                                        algarismos_na_enumeracao.append(plv)
                                        i += 1 #ao fim da avaliação da palavra atual passa para a próxima (até que se encontre um novo termo de interesse ou o fim do texto). essa redundância com o primeiro loop é devido ao fato de que alguns termos enumeram com números, outros com letras e outros com algarismos romanos. mantendo o controle da busca dentro da condição a avaliação fica mais simples.
                                        comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                                        contador_sem_termo_interesse = 0
                                        while i < len(palavras) - 1 and not comeca_com_termo and contador_sem_termo_interesse < 3: #enquanto ainda for possivelmente um conteúdo da enumeração do termo atual
                                                if avaliaTerminacao(palavras[i], chars_de_terminacao): 
                                                        i += 1 #ao sair do while há um i -= 1
                                                        break
                                                        flag_terminacao = True
                                                possiveis_romanos = re.split('\W+', palavras[i])
                                                tem_romano = False
                                                for plv in possiveis_romanos:
                                                        if all(c in "xivlcdm" for c in plv) and plv != '':
                                                                algarismos_na_enumeracao.append(plv)
                                                                tem_romano = True
                                                if tem_romano == False:
                                                        contador_sem_termo_interesse += 1
                                                i += 1 #pode ter saído do loop ou por ter acabado o texto ou por ter encontrado um novo termo
                                                comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                                        i -= 1
                                        print(algarismos_na_enumeracao)
                                        adicionaNoArquivo(sys.argv[1] + '/' + arqv, termo_atual, algarismos_na_enumeracao)
                                        pass
                                #####################################
                                # FIM: avaliação no caso de Incisos #
                                #####################################



                                ########################################
                                # INÍCIO: avaliação no caso de Alíneas #
                                ########################################
                                #partido do pressuposto que as alíneas serão enumeradas entre áspas duplas ou simples
                                elif posicao_na_lista in [1, 2]: 
                                        termo_atual = dicionario_termos[posicao_na_lista]
                                        letras_na_enumeracao = [] #salva todas letras da enumeração do termo atual

                                        possiveis_alineas = re.findall('“([^"]*)”', palavras[i]) #obtém tudo que está entre duas àspas na palavra atual
                                        for plv in possiveis_alineas:
                                                if len(plv) < 4 and len(plv) > 0:
                                                        letras_na_enumeracao.append(plv)
                                        i += 1 #ao fim da avaliação da palavra atual passa para a próxima (até que se encontre um novo termo de interesse ou o fim do texto). essa redundância com o primeiro loop é devido ao fato de que alguns termos enumeram com números, outros com letras e outros com algarismos romanos. mantendo o controle da busca dentro da condição a avaliação fica mais simples.
                                        comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                                        contador_sem_termo_interesse = 0
                                        while i < len(palavras) - 1 and not comeca_com_termo and contador_sem_termo_interesse < 3: #enquanto ainda for possivelmente um conteúdo da enumeração do termo atual
                                                if avaliaTerminacao(palavras[i], chars_de_terminacao): 
                                                        i += 1 #ao sair do while há um i -= 1
                                                        break
                                                        flag_terminacao = True
                                                possiveis_alineas = re.findall('“([^"]*)”', palavras[i]) #obtém tudo que está entre duas àspas na palavra atual
                                                tem_alinea = False
                                                for plv in possiveis_alineas:
                                                        if len(plv) < 4 and len(plv) > 0:
                                                                letras_na_enumeracao.append(plv)
                                                                tem_alinea = True

                                                if tem_alinea == False:
                                                        contador_sem_termo_interesse += 1
                                                i += 1 #pode ter saído do loop ou por ter acabado o texto ou por ter encontrado um novo termo
                                                comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                                        i -= 1
                                        print(letras_na_enumeracao)
                                        adicionaNoArquivo(sys.argv[1] + '/' + arqv, termo_atual, letras_na_enumeracao)
                                        pass
                                
                                #####################################
                                # FIM: avaliação no caso de Alíneas #
                                #####################################
                                print(termo_atual)

                        i += 1
                        

                with open(sys.argv[1] + '/' + arqv, 'a') as arquivo:
                        arquivo.write('\n\n%$#@!')



if __name__ == "__main__":
        main()
