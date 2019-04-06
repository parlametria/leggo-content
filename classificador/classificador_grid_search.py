#formatação
import numpy as np
import re
from preprocessamento import tokenizador #tokenizador próprio

#embedding TF-IDF
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

#treinos
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

#resultados
from sklearn import metrics


################################## leituras
with open('PLs_categorias_Leggo.txt', 'r') as arquivo:
	linhas = arquivo.readlines()


lista_textos = []
dicionario_categorias = {}
nomes_documentos = []
for linha in linhas:#[:15]:
	aux = linha.split('***') #[0] -> nome do documento, [1] -> label no Leggo
	
	with open('../../../Dados_Finais_ÀgoraDigital_3317/FINAL_textos_iniciais/' + aux[0] + '_.pdf.txt', 'r') as arquivo:
		texto = arquivo.read()
	
	nomes_documentos.append(aux[0])
	lista_textos.append(texto)
	dicionario_categorias[aux[1][:-1]] = 0


################################## formatação de labels
i = 1
for chave in dicionario_categorias.keys():
	dicionario_categorias[chave] = i #atribuição de valor numérico para cada categoria
	i += 1

#print(dicionario_categorias)
Y = []
for linha in linhas:#[:15]:
	aux = linha.split('***')
	Y.append(dicionario_categorias[aux[1][:-1]])

#print(Y)
Y = np.array(Y)

#vetorizador = TfidfVectorizer()
#X = vetorizador.fit_transform(lista_textos).toarray()
X = np.array(lista_textos)


################################## treinos
kf_5 = KFold(n_splits = 5, shuffle = True)

#grid search SVM
print('\nTreino SVM')
C = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
kernels = ['linear', 'rbf', 'sigmoid']
melhor_acuracia = -1.0
melhores_parametros = {'gamma' : 'auto', 'decision_function_shape' : 'ovo'}
for C_atual in C:
	for kernel_atual in kernels:
		print('SVM')
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

		with open('SVM_parametros_2.txt', 'w') as arquivo:
			arquivo.write(str(melhores_parametros))		


#grid search KNN
print('\nTreino KNN')
melhor_acuracia = -1.0
n_vizinhos = [3, 5]
pesos = ['uniform', 'distance']
p_norma = [1, 2]
melhores_parametros = {}
for N in n_vizinhos:
	for peso in pesos:
		for norma in p_norma:
			print('KNN')
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

			with open('KNN_parametros_2.txt', 'w') as arquivo:
				arquivo.write(str(melhores_parametros))
