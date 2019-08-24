import string
import re
import os
import sys


def obtem_lista_termos(arqv):
        '''
                Lê de um arquivo processado pelo parser de itens os itens, que estão contidos entre os tokens de separação '%$#@!' e '!@#$%'
                Retorna a lista dos termos
        '''

        termos_em_ordem = []
        with open(sys.argv[1] + '/' + arqv, 'r') as arquivo:
                texto = arquivo.readlines()
                adicionar = False
                for linha in texto:
                        linha = linha.replace('\n', '')
                        if linha == '%$#@!':
                                adicionar = False

                        if adicionar and linha != '':
                                termos_em_ordem.append(linha)

                        if linha == '!@#$%':
                                adicionar = True
        
        return termos_em_ordem



def main():
        TAMANHO_OPCOES_CONJUNTO = 4

        hierarquia = { 
                'artigo': 0,
                'inciso': 1,
                'alinea': 2,
                'paragrafo': 3
        }

        pasta = os.listdir(sys.argv[1])

        for arqv in pasta:
                termos_em_ordem = obtem_lista_termos(arqv)
                todos_conjuntos_termos = []
                
                
                i = 0
                if termos_em_ordem[i].split('_')[0] == 'artigo':
                        heuristica_sequencial = True
                else:  
                        heuristica_sequencial = False

                if heuristica_sequencial: #o fluxo muda dependendo se a enumeração começa com artigo ou não, pois isso revela como o(a) redator(a) fará a enumeração
                        conjunto_atual = [''] * TAMANHO_OPCOES_CONJUNTO #uma posição para cada termo possível
                        conjunto_atual[hierarquia[termos_em_ordem[i].split('_')[0]]] = termos_em_ordem[i]
                        i += 1

                        while i < len(termos_em_ordem):
                                termo_atual = termos_em_ordem[i].split('_')[0]
                                termo_anterior = termos_em_ordem[i - 1].split('_')[0]
                                if hierarquia[termo_atual] > hierarquia[termo_anterior]: #ou seja, se o termo atual estiver abaixo do último termo na hierarquia
                                        conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i]
                                else: #senão, isso indica o fim de um conjunto fechado de termos
                                        todos_conjuntos_termos.append(tuple(conjunto_atual))

                                        for j in range(hierarquia[termo_atual], len(conjunto_atual)): #limpa o vetor a partir da posição em que o termo atual entraria
                                                conjunto_atual[j] = ''
                                        conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i] #deixa os termos acima na hierarquia ainda salvos, mas substitui o atual

                                i += 1

                else: #senão, adotamos a heurística sequencial inversa (a pessoa começa a enumeração pelo nível mais baixo na hierarquia
                        conjunto_atual = [''] * TAMANHO_OPCOES_CONJUNTO #uma posição para cada termo possível
                        conjunto_atual[hierarquia[termos_em_ordem[i].split('_')[0]]] = termos_em_ordem[i]
                        i += 1

                        print(conjunto_atual)
                        while i < len(termos_em_ordem):
                                termo_atual = termos_em_ordem[i].split('_')[0]
                                termo_anterior = termos_em_ordem[i - 1].split('_')[0]
                                print(termo_atual + ' ' + termo_anterior)
                                if hierarquia[termo_atual] < hierarquia[termo_anterior]: #ou seja, se o termo atual estiver acima do último termo na hierarquia
                                        
                                        conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i]
                                else: #senão, isso indica o fim de um conjunto fechado de termos
                                        todos_conjuntos_termos.append(tuple(conjunto_atual))

                                        for j in range(0, hierarquia[termo_atual]): #limpa o vetor a partir da posição em que o termo atual entraria
                                                conjunto_atual[j] = ''
                                        conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i] #deixa os termos abaixo na hierarquia ainda salvos, mas substitui o atual

                                i += 1  

                arquivo = open(sys.argv[1] + '/' + arqv, 'a')
                arquivo.write('\n' "__INICIO_AGREGADOR__\n")
                todos_conjuntos_termos_unicos = [] #contém apenas conjuntos de termos únicos, sem repetição
                for conj in todos_conjuntos_termos:
                        if conj not in todos_conjuntos_termos_unicos:
                                arquivo.write(str(conj) + '\n')
                                todos_conjuntos_termos_unicos.append(conj)
                arquivo.write("__FIM_AGREGADOR__")
                arquivo.close()



if __name__ == "__main__":
        main()
