'''
Classificador CRF
'''


import pycrfsuite
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
import numpy as np
import os


import spacy
from spacy.lang.pt.examples import sentences 

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


def criador_de_features(documento, posicao_do_par, doc_nlp):
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
			'anterior_e_digito=%s' % palavra_anterior.isdigit()
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
			'posterior_e_digito=%s' % palavra_posterior.isdigit()
		])

		'''pos_tag_post = ''
		for token in doc_nlp:
			if token.text == palavra_posterior:
				pos_tag_post = token.pos_
		if pos_tag_post != '':
			features.extend(['pos_tag=' + pos_tag_post])
		'''
	

	return features


def resultados_parciais(arquivo_modelo, X_teste, y_teste):
	'''
	Imprime os resultados (precisão e recall)
	'''


	#labels_possiveis = ['O', 'B-SUB', 'B-MOD', 'B-ADD', 'B-SUP', 'I-SUB', 'I-MOD', 'I-ADD', 'I-SUP', 'E-SUB', 'E-MOD', 'E-ADD', 'E-SUP']
	labels_possiveis = ['O', 'B-MOD', 'B-ADD', 'B-SUP', 'I-MOD', 'I-ADD', 'I-SUP', 'E-MOD', 'E-ADD', 'E-SUP']
	mapa_labels = {
		'O': 0,
		'B-MOD': 1,
		'B-ADD': 2,
		'B-SUP': 3,
		'I-MOD': 4,
		'I-ADD': 5,
		'I-SUP': 6,
		'E-MOD': 7,
		'E-ADD': 8,
		'E-SUP': 9
	}

	tagger = pycrfsuite.Tagger()
	tagger.open(arquivo_modelo)


	y_pred = [tagger.tag(unidade_x_teste) for unidade_x_teste in X_teste] #predições
	y_pred_np = np.array([mapa_labels[y_pred_i] for preds_documento in y_pred for y_pred_i in preds_documento]) #formato para avaliação do classification_report
	y_teste_np = np.array([mapa_labels[y_teste_i] for labels_documento in y_teste for y_teste_i in labels_documento]) #labels corretas

	dic_results = classification_report(y_teste_np, y_pred_np, labels = np.arange(len(mapa_labels)), target_names = labels_possiveis, output_dict = True)
	#print(dic_results)

	return dic_results
	
	

def resultados_validacao_cruzada(todos_resultados):
	labels_possiveis = ['O', 'B-MOD', 'B-ADD', 'B-SUP', 'I-MOD', 'I-ADD', 'I-SUP', 'E-MOD', 'E-ADD', 'E-SUP']
	dic_resultados_kfold = {}
	for label_atual in labels_possiveis:
		dic_resultados_kfold[label_atual] = {}


	for label_atual in labels_possiveis:
		dic_resultados_kfold[label_atual]['precision'] = 0
		dic_resultados_kfold[label_atual]['recall'] = 0
		dic_resultados_kfold[label_atual]['f1-score'] = 0


	for i in range(len(todos_resultados)):
		for label_atual in labels_possiveis:
			dic_resultados_kfold[label_atual]['precision'] += todos_resultados[i][label_atual]['precision'] / 5.0
			dic_resultados_kfold[label_atual]['recall'] += todos_resultados[i][label_atual]['recall'] / 5.0
			dic_resultados_kfold[label_atual]['f1-score'] += todos_resultados[i][label_atual]['f1-score'] / 5.0
	
	
	print('\t\t\t\tResultados 5-Fold\n')
	print('label \t\t precision \t\t recall \t\t f1-score')
	for label in dic_resultados_kfold.keys():
		print(label + '\t\t' + str(round(dic_resultados_kfold[label]['precision'], 4)) + '\t\t\t' + str(round(dic_resultados_kfold[label]['recall'], 4)) + '\t\t\t' + str(round(dic_resultados_kfold[label]['f1-score'], 4)))



def main():
	'''
	Função principal
	'''

	np.random.seed(123)
	nlp = spacy.load('pt_core_news_sm')

	pares_palavra_tag = []
	for arquivo in os.listdir('tagFiles/'): #diretório com arquivos de treino e teste
		#print(arquivo)
		pares_palavra_tag += leitura_de_dados('tagFiles/' + arquivo)


	#pares_com_O = [tupla for tupla in pares_palavra_tag if tupla[1] == 'O'] #pares apenas com out of segment
	#pares_palavra_tag = [tupla for tupla in pares_palavra_tag if tupla[1] != 'O'] #pares apenas com segmentos com conteúdo informativo
	
	documentos = separa_em_blocos(pares_palavra_tag) #cada segmento é um documento, as tags B e E indicam o início e o fim de um segmento
	

	X = [] #lista de lista, cada lista contém as features de palavras de um mesmo documento
	y = [] #lista de lista, cada lista contém as labels de palavras de um mesmo documento
	for documento in documentos:
		Xi = [] #vetor de features, cada posição contém as features de uma palavra
		yi = [] #vetor de labels, cada posição contém as labels de uma palavra
		aux = list(zip(*documento))[0]
		doc_nlp = nlp(' '.join(aux))
		for i in range(len(documento)):
			Xi.append(criador_de_features(documento, i, doc_nlp))
			yi.append(documento[i][1])
		X.append(Xi)
		y.append(yi)


	#5-Fold
	X = np.array(X)
	y = np.array(y)
	kf_5 = KFold(n_splits = 5, shuffle = True)
	todos_resultados = [] #sumarização dos resultados
	for indice_treino, indice_teste in kf_5.split(X):
		print('em treino...')
		X_treino, X_teste = X[indice_treino], X[indice_teste]
		y_treino, y_teste = y[indice_treino], y[indice_teste]	



		modelo = pycrfsuite.Trainer(verbose = True)


		for unidade_x, unidade_y in zip(X_treino, y_treino):
			modelo.append(unidade_x, unidade_y)


		modelo.set_params({
			'c1': 0.1,
			'c2': 0.01,
			'max_iterations': 1000,
			#'all_possible_transitions': True
			'feature.possible_transitions': True
		})

		modelo.train('modelo.model')

		dic_results = resultados_parciais('modelo.model', X_teste, y_teste)

		todos_resultados.append(dic_results)


	resultados_validacao_cruzada(todos_resultados)
	
	


if __name__ == "__main__":
	main()
