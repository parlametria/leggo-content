'''
Script puramente para teste de saída de predições
'''

import pycrfsuite
import numpy as np
import os


def leitura_de_dados(arquivo_de_entrada):
	'''
	Lê o arquivo com os dados o qual contém, em cada linha, um par palavra-tag.
	Retorna uma lista de pares palavra-tag.
	'''

	with open(arquivo_de_entrada, 'r') as arquivo:
		linhas = arquivo.readlines()

	pares_palavra_tag = []
	for linha in linhas:
		tupla = tuple(linha.split())
		#print(tupla)
		pares_palavra_tag.append(tupla)

	return pares_palavra_tag


def separa_em_blocos(pares_palavra_tag):
	'''
	Separa o documento em diferentes blocos/segmentos.
	Retorna uma lista de documentos/blocos.
	'''

	documentos = [] 
	documento = []
	for i in range(len(pares_palavra_tag)):
		documento.append(pares_palavra_tag[i])
		if('B-' in pares_palavra_tag[i][1] and len(documento) > 1): #se encontrar um Begin (depois de uma sequência de Outs ou NÃO logo após um End, len(documento) > 1) 
			aux = documento.pop()
			documentos.append(documento)
			documento = []
			documento.append(aux)
		else:
			if('E-' in pares_palavra_tag[i][1]): #se encontrar um End
				documentos.append(documento)
				documento = []

	return documentos



def criador_de_features(documento, posicao_do_par):
	'''
	Dado um documento/bloco e a posição do par palavra-tag atual obtém as features desse par.
	Retorna uma lista de features.
	'''

	palavra = documento[posicao_do_par][0]
	tag = documento[posicao_do_par][1]

	features = [ 
		'bias',
		'palavra_minusculo=' + palavra.lower(),
		'esta_em_maiusculo=%s' % palavra.isupper(),
		'e_titulo=%s' % palavra.istitle(),
		'e_digito=%s' % palavra.isdigit()
	] #features genéricas, servem para qualquer palavra no documento/bloco, independentemente de sua posição

	#aqui podem ser acrescentadas features dependendo da posição da palavra no documento/bloco
	#por exemplo, palavras que estão entre as primeira e última palavras do bloco podem tomar como features as palavras ao redor

	return features



def teste_predicao(arquivo_modelo, documentos, X_teste, y_teste):
	'''
	Função auxiliar, apenas para teste de saída de predições.
	'''

	tagger = pycrfsuite.Tagger()
	tagger.open(arquivo_modelo)
	y_pred = [tagger.tag(unidade_x_teste) for unidade_x_teste in X_teste] #predições

	k = 0 #iterador de documentos
	for doc in documentos:
		i = 0 #iterador de palavras em cada documento
		for palavra in doc:
			with open('predicoes.txt', 'a') as arquivo:
				arquivo.write(str(list(zip(palavra, y_pred[k][i]))))
				arquivo.write('\n')
			i += 1
		k += 1


def main():
	np.random.seed(123)

	pares_palavra_tag = []
	for arquivo in os.listdir('tagFiles/'):
		print(arquivo)
		pares_palavra_tag += leitura_de_dados('tagFiles/' + arquivo)


	#pares_com_O = [tupla for tupla in pares_palavra_tag if tupla[1] == 'O'] #pares apenas com out of segment
	#pares_palavra_tag = [tupla for tupla in pares_palavra_tag if tupla[1] != 'O'] #pares apenas com segmentos com conteúdo informativo
	
	documentos = separa_em_blocos(pares_palavra_tag) #cada segmento é um documento, as tags B e E indicam o início e o fim de um segmento
	

	X = [] #lista de lista, cada lista contém as features de palavras de um mesmo documento
	y = [] #lista de lista, cada lista contém as labels de palavras de um mesmo documento
	for documento in documentos:
		Xi = [] #vetor de features, cada posição contém as features de uma palavra
		yi = [] #vetor de labels, cada posição contém as labels de uma palavra
		for i in range(len(documento)):
			Xi.append(criador_de_features(documento, i))
			yi.append(documento[i][1])
		X.append(Xi)
		y.append(yi)


	predicao('modelo10000.model', documentos, X, y)


if __name__ == "__main__":
	main()



