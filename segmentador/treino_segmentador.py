'''
Treina um classificador CRF utilizando como documento uma janela de tamanho k.
Uma janela com k = 4, por exemplo, significa que o bloco possui uma palavra central, as quatro anteriores e as quatro posteriores.
'''


import pycrfsuite
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
import numpy as np
import os
import sys


#import spacy
#from spacy.lang.pt.examples import sentences 
import pickle

def leitura_de_dados(arquivo_de_entrada):
	'''
	Lê o arquivo com os dados o qual contém, em cada linha, um par palavra-tag.
	Retorna uma lista de pares palavra-tag.
	'''

	with open(arquivo_de_entrada, 'r') as arquivo:
		linhas = arquivo.readlines()

	pares_palavra_tag = []
	for linha in linhas:
		palavra_tag = linha.split()
		if 'B-' in palavra_tag[1]:
			palavra_tag[1] = 'I' #inicia um bloco
		else:
			palavra_tag[1] = 'O' #não inicia um bloco
		tupla = tuple(palavra_tag)
		#print(tupla)
		pares_palavra_tag.append(tupla)

	return pares_palavra_tag



def separa_em_blocos(pares_palavra_tag, tamanho_janela = 1):
	'''
	Separa o documento em diferentes blocos/segmentos.
	Retorna uma lista de documentos/blocos.
	'''

	documentos = []
	for i in range(tamanho_janela):
		documentos.append(pares_palavra_tag[0:i] + [pares_palavra_tag[i]] + pares_palavra_tag[(i + 1):(i + 1 + tamanho_janela)]) 
	for i in range(tamanho_janela, len(pares_palavra_tag) - tamanho_janela):
		documentos.append(pares_palavra_tag[(i - tamanho_janela):i] + [pares_palavra_tag[i]] + pares_palavra_tag[(i + 1):(i + 1 + tamanho_janela)]) #os blocos centrais possuem a palavra central + as palavras de borda
	for i in range(len(pares_palavra_tag) - tamanho_janela, len(pares_palavra_tag)):
		documentos.append(pares_palavra_tag[(i - tamanho_janela):i] + [pares_palavra_tag[i]] + pares_palavra_tag[(i + 1):(i + tamanho_janela)])


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
	else:
		features.append('BOS') #início de documento

	if posicao_do_par < len(documento) - 1:
		palavra_posterior = documento[posicao_do_par + 1][0]
		
		features.extend([
			'palavra_posterior_minusculo=' + palavra_posterior.lower(),
			'posterior_esta_em_maiusculo=%s' % palavra_posterior.isupper(),
			'posterior_e_titulo=%s' % palavra_posterior.istitle(),
			'posterior_e_digito=%s' % palavra_posterior.isdigit(),
			'pos_tag_post=' + pos_tags_documento[posicao_do_par + 1][1]
		])
	else:
		features.append('EOS') #fim de documento

	
	return features


def resultados_parciais(arquivo_modelo, X_teste, y_teste):
	'''
	Imprime os resultados do modelo treinado com o fold atual
	'''

	labels_possiveis = ['O', 'I']
	mapa_labels = {
		'O': 0,
		'I': 1
	}

	tagger = pycrfsuite.Tagger()
	tagger.open(arquivo_modelo)


	y_pred = [tagger.tag(unidade_x_teste) for unidade_x_teste in X_teste] #predições
	y_pred_np = np.array([mapa_labels[y_pred_i] for preds_documento in y_pred for y_pred_i in preds_documento]) #formato para avaliação do classification_report
	y_teste_np = np.array([mapa_labels[y_teste_i] for labels_documento in y_teste for y_teste_i in labels_documento]) #labels corretas

	dic_results = classification_report(y_teste_np, y_pred_np, labels = np.arange(len(mapa_labels)), target_names = labels_possiveis, output_dict = True)


	return dic_results



def resultados_validacao_cruzada(todos_resultados, caminho_salvar):
	'''
	Salva os resultados finais do modelo treinado
	'''

	labels_possiveis = ['O', 'I']
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

	with open(caminho_salvar, 'w') as arq:
		arq.write('\t\t\t\tResultados 5-Fold\n')
		arq.write('label \t\t precision \t\t recall \t\t f1-score\n')
		for label in dic_resultados_kfold.keys():
			arq.write(label + '\t\t' + str(round(dic_resultados_kfold[label]['precision'], 4)) + '\t\t\t' + str(round(dic_resultados_kfold[label]['recall'], 4)) + '\t\t\t' + str(round(dic_resultados_kfold[label]['f1-score'], 4)) + '\n')
		


def main():
	'''
	Função principal
	'''

	np.random.seed(123)
	#nlp = spacy.load('pt_core_news_sm')

	pares_palavra_tag = []
	for arquivo in os.listdir(sys.argv[1] + '/'): #diretório com arquivos de treino e teste
		pares_palavra_tag += leitura_de_dados(sys.argv[1] + '/' + arquivo)

	
	janelas = [4] #lista com tamanhos de janela que se deseja testar, no caso já sabe-se que a janela de tamanho 4 obteve um bom desempenho
	for tamanho_janela in janelas:
		documentos = separa_em_blocos(pares_palavra_tag, tamanho_janela) #cada segmento é um documento

		tagger = pickle.load(open("tagger_portugues.pkl", "rb"))
	
		X = [] #lista de listas, cada lista contém as features de palavras de um mesmo documento
		y = [] #lista de listas, cada lista contém as labels de palavras de um mesmo documento
		for documento in documentos:
			Xi = [] #vetor de features, cada posição contém as features de uma palavra
			yi = [] #vetor de labels, cada posição contém as labels de uma palavra
			pos_tags_documento = tagger.tag(list(zip(*documento))[0])
			for i in range(len(documento)):
				Xi.append(criador_de_features(documento, i, pos_tags_documento))
				yi.append(documento[i][1])
			X.append(Xi)
			y.append(yi)

		X = np.array(X)
		y = np.array(y)
		kf_5 = KFold(n_splits = 5, shuffle = True) #5-Fold
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
				'max_iterations': 100
				#'all_possible_transitions': True
				#'feature.possible_transitions': True
			})

			modelo.train(sys.argv[2])

			dic_results = resultados_parciais(sys.argv[2], X_teste, y_teste)

			todos_resultados.append(dic_results)
			

		#treino final, utilizando todos dados
		modelo = pycrfsuite.Trainer(verbose = True)
		for unidade_x, unidade_y in zip(X, y):
			modelo.append(unidade_x, unidade_y)
		modelo.train(sys.argv[2])
		modelo.set_params({
				'c1': 0.1,
				'c2': 0.01,
				'max_iterations': 1000
				#'all_possible_transitions': True
				#'feature.possible_transitions': True
			})
		modelo.train(sys.argv[2])

		resultados_validacao_cruzada(todos_resultados, sys.argv[3] + '/' + str(tamanho_janela) + '.txt')
	

	
if __name__ == "__main__":
	main()



