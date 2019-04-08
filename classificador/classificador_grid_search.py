#formatação de labels
import numpy as np
from preprocessamento import tokenizador #tokenizador próprio

#embedding TF-IDF
#from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

#treinos
from sklearn.model_selection import KFold
#from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

#resultados
#from sklearn import metrics


def leitura_dados():
	'''
	Lê os dados: nomes das PLs e suas categorias, além dos textos
	Retorno: linhas do arquivo com nomes e categorias, conteúdos dos textos, dicionário com as categorias possíveis, nomes dos documentos separados
	'''

	with open('arquivo_com_PLs_e_suas_categorias_LegGo', 'r') as arquivo:
		linhas = arquivo.readlines()


	lista_textos = []
	dicionario_categorias = {}
	nomes_documentos = []
	for linha in linhas:#[:15]:
		aux = linha.split('***') #[0] -> nome do documento, [1] -> label no Leggo
	
		with open('caminho_para_textos_iniciais_das_PLs' + aux[0] + '_.pdf.txt', 'r') as arquivo:
			texto = arquivo.read()
	
		nomes_documentos.append(aux[0])
		lista_textos.append(texto)
		dicionario_categorias[aux[1][:-1]] = 0

	return linhas, lista_textos, dicionario_categorias, nomes_documentos
	

def labels_formatadas(dicionario_categorias, linhas):
	'''
	Formata as labels (categorias) para treino
	Retorno: vetor numérico com a categoria de cada PL
	'''

	Y = []
	for linha in linhas:#[:15]:
		aux = linha.split('***')
		Y.append(dicionario_categorias[aux[1][:-1]])

	return np.array(Y)


def grid_search_svm(X, Y, C, kernels):
	'''
	Faz um busca pelos melhores parâmetros de uma SVM dentre os parâmetros escolhidos
	Retorno: melhores parâmetros da SVM
	'''

	kf_5 = KFold(n_splits = 5, shuffle = True)
	print('\nTreino SVM')
	melhor_acuracia = -1.0
	melhores_parametros = {'gamma' : 'auto', 'decision_function_shape' : 'ovo'}
	for C_atual in C:
		for kernel_atual in kernels:
			print('SVM em treino...')
			acuracia_media = 0.0
			for indice_treino, indice_teste in kf_5.split(X):
				X_treino, X_teste = X[indice_treino], X[indice_teste]
				Y_treino, Y_teste = Y[indice_treino], Y[indice_teste]

				vetorizador = TfidfVectorizer(analyzer = 'word', tokenizer = tokenizador)
				vetorizador.fit(X_treino) #o vetor tem apenas as posições do treino e isso é salvo no objeto vetorizador
				X_treino = vetorizador.transform(X_treino)
				X_teste = vetorizador.transform(X_teste) #as posições (palavras) que existem no teste mas não no treino são ignoradas

				classificador_svm = svm.SVC(gamma = 'auto', decision_function_shape = 'ovo', C = C_atual, kernel = kernel_atual)
				classificador_svm.fit(X_treino, Y_treino)
				#print(nomes_documentos[indice_treino])
	
				acuracia = classificador_svm.score(X_teste, Y_teste)
				acuracia_media += acuracia
		
			acuracia_media /= 5.0
			if(acuracia_media > melhor_acuracia):
				melhores_parametros['C'] = C_atual
				melhores_parametros['kernel'] = kernel_atual
				melhores_parametros['acuracia'] = acuracia_media
				melhor_acuracia = acuracia_media

			print(acuracia_media)

	return melhores_parametros


def grid_search_knn(X, Y, n_vizinhos, pesos, p_norma):
	'''
	Faz um busca pelos melhores parâmetros de um KNN dentre os parâmetros escolhidos
	Retorno: melhores parâmetros do KNN
	'''

	kf_5 = KFold(n_splits = 5, shuffle = True)
	print('\nTreino KNN')
	melhor_acuracia = -1.0
	melhores_parametros = {}
	for N in n_vizinhos:
		for peso in pesos:
			for norma in p_norma:
				print('KNN em treino...')
				acuracia_media = 0.0
				for indice_treino, indice_teste in kf_5.split(X):
					X_treino, X_teste = X[indice_treino], X[indice_teste]
					Y_treino, Y_teste = Y[indice_treino], Y[indice_teste]

					vetorizador = TfidfVectorizer(analyzer = 'word', tokenizer = tokenizador)
					vetorizador.fit(X_treino) #o vetor tem apenas as posições do treino e isso é salvo no objeto vetorizador
					X_treino = vetorizador.transform(X_treino)
					X_teste = vetorizador.transform(X_teste) #as posições (palavras) que existem no teste mas não no treino são ignoradas

					#knn
					classificador_knn = KNeighborsClassifier(n_neighbors = N, weights = peso, p = norma)
					classificador_knn.fit(X_treino, Y_treino)

					acuracia = classificador_knn.score(X_teste, Y_teste)
					acuracia_media += acuracia

				acuracia_media /= 5.0
				if(acuracia_media > melhor_acuracia):
					melhores_parametros['n_vizinhos'] = N
					melhores_parametros['pesos'] = peso
					melhores_parametros['norma'] = norma
					melhores_parametros['acuracia'] = acuracia_media
					melhor_acuracia = acuracia_media

				print(acuracia_media)

	return melhores_parametros



def main():
	################################## leituras
	linhas, lista_textos, dicionario_categorias, nomes_documentos = leitura_dados()


	################################## formatação de labels
	i = 1
	for chave in dicionario_categorias.keys():
		dicionario_categorias[chave] = i #atribuição de valor numérico para cada categoria
		i += 1

	Y = labels_formatadas(dicionario_categorias, linhas) 
	X = np.array(lista_textos)


	################################## grid searches e resultados
	#svm
	C = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
	kernels = ['linear', 'rbf', 'sigmoid']
	melhores_parametros_svm = grid_search_svm(X, Y, C, kernels)
	with open('arquivo_para_salvar_melhores_parametros_svm', 'w') as arquivo:
		arquivo.write(str(melhores_parametros_svm))		

	#knn
	n_vizinhos = [3, 5]
	pesos = ['uniform', 'distance']
	p_norma = [1, 2]
	melhores_parametros_knn = grid_search_knn(X, Y, n_vizinhos, pesos, p_norma)
	with open('arquivo_para_salvar_melhores_parametros_knn', 'w') as arquivo:
		arquivo.write(str(melhores_parametros_knn))


if __name__ == "__main__":
	main()
