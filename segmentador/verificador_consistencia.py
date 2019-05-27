import os
import nltk
import numpy as np
import pickle
import pycrfsuite


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


#def criador_de_features(documento, posicao_do_par, doc_nlp):
def criador_de_features(documento, posicao_do_par, pos_tags_documento):
	'''
	Dado um documento/bloco e a posição do par palavra-tag atual obtém as features desse par.
	Retorna uma lista de features.
	'''
	
	palavra = documento[posicao_do_par][0]
	tag = documento[posicao_do_par][1]
	pos_tag = pos_tags_documento[posicao_do_par][1]



	features = [ 
		'bias',
		'palavra_minusculo=' + palavra.lower(),
		'esta_em_maiusculo=%s' % palavra.isupper(),
		'e_titulo=%s' % palavra.istitle(),
		'e_digito=%s' % palavra.isdigit(),
		'pos_tag=' + pos_tag
	] #features genéricas, servem para qualquer palavra no documento/bloco, independentemente de sua posição
	
	'''pos_tag = ''
	for token in doc_nlp:
		if token.text == palavra:
			pos_tag = token.pos_
	if pos_tag != '': #se há pos tagging para essa palavra (necessário conferir já que o nlp() do spacy tokeniza diferente do arquivo de entrada)
		features.extend(['pos_tag=' + pos_tag])
	'''

	#aqui podem ser acrescentadas features dependendo da posição da palavra no documento/bloco
	#por exemplo, palavras que estão entre as primeira e última palavras do bloco podem tomar como features as palavras ao redor
	
	if posicao_do_par > 0: #se houver palavras anteriores
		palavra_anterior = documento[posicao_do_par - 1][0]
		
		features.extend([
			'palavra_anterior_minusculo=' + palavra_anterior.lower(),
			'anterior_esta_em_maiusculo=%s' % palavra_anterior.isupper(),
			'anterior_e_titulo=%s' % palavra_anterior.istitle(),
			'anterior_e_digito=%s' % palavra_anterior.isdigit(),
			'pos_tag_ant=' + pos_tags_documento[posicao_do_par - 1][1]
		])

		'''pos_tag_ant = ''
		for token in doc_nlp:
			if token.text == palavra_anterior:
				pos_tag_ant = token.pos_
		if pos_tag_ant != '':
			features.extend(['pos_tag=' + pos_tag_ant])
		'''

		

	if posicao_do_par < len(documento) - 1:
		palavra_posterior = documento[posicao_do_par + 1][0]
		
		features.extend([
			'palavra_posterior_minusculo=' + palavra_posterior.lower(),
			'posterior_esta_em_maiusculo=%s' % palavra_posterior.isupper(),
			'posterior_e_titulo=%s' % palavra_posterior.istitle(),
			'posterior_e_digito=%s' % palavra_posterior.isdigit(),
			'pos_tag_post=' + pos_tags_documento[posicao_do_par + 1][1]
		])

		'''pos_tag_post = ''
		for token in doc_nlp:
			if token.text == palavra_posterior:
				pos_tag_post = token.pos_
		if pos_tag_post != '':
			features.extend(['pos_tag=' + pos_tag_post])
		'''
	

	return features


def verifica_consistencia(arquivo_modelo, X_teste):
	tagger = pycrfsuite.Tagger()
	tagger.open(arquivo_modelo)

	y_pred = [tagger.tag(unidade_x_teste) for unidade_x_teste in X_teste] #predições

	#print(y_pred)
	#print(len(y_pred))


	for bloco in y_pred:
		if bloco[0] == 'O':
			inc = False
			for tag in bloco:
				if tag != 'O':
					inc = True
					print('Inconsistente')
					break

			if(not inc):
				print('Todo Consistente')
		else:
			if bloco[0][0] != 'B':
				print('Inconsistente: não começa com B')
			if bloco[len(bloco) - 1][0] != 'E':
				print('Inconsistente: não termina em E')
			else: #se começa com B e termina em E
				inc = False
				for tag in bloco[1:len(bloco) - 2]:
					if tag[0] != 'I':
						inc = True
						print('Inconsistente: não tem só I no meio')
						pass

				if(not inc):
					print('Todo Consistente')

		

def main():
	nomes_arquivos = os.listdir('arquivos_testar_consistencia/')
	pares_palavra_tag = []
	for arquivo in nomes_arquivos: #diretório com arquivos de treino e teste
		#print(arquivo)
		pares_palavra_tag += leitura_de_dados('arquivos_testar_consistencia/' + arquivo)


	documentos = separa_em_blocos(pares_palavra_tag) #cada segmento é um documento, as tags B e E indicam o início e o fim de um segmento
	tagger = pickle.load(open("tagger_portugues.pkl", "rb"))

	X = [] #lista de lista, cada lista contém as features de palavras de um mesmo documento
	for documento in documentos:
		Xi = [] #vetor de features, cada posição contém as features de uma palavra
		pos_tags_documento = tagger.tag(list(zip(*documento))[0])
		for i in range(len(documento)):
			Xi.append(criador_de_features(documento, i, pos_tags_documento))
		X.append(Xi)


	verifica_consistencia('modelo.model', X)

if __name__ == "__main__":
	main()

