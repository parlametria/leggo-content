#formatação
import numpy as np
import spacy
from spacy.tokenizer import Tokenizer
import re

#embedding TF-IDF
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

#treinos
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

#resultados
from sklearn import metrics

#tokenização
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


#formatação de labels
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
kf_5 = KFold(n_splits = 5, shuffle = True)
for indice_treino, indice_teste in kf_5.split(X):
	X_treino, X_teste = X[indice_treino], X[indice_teste]
	Y_treino, Y_teste = Y[indice_treino], Y[indice_teste]

	vetorizador = TfidfVectorizer()
	vetorizador.fit(X_treino)
	X_treino = vetorizador.transform(X_treino)
	X_teste = vetorizador.transform(X_teste)

	#treinos
	#svm
	classificador_svm = svm.SVC(gamma = 'auto', decision_function_shape = 'ovo')
	classificador_svm.fit(X_treino, Y_treino)
	#print(nomes_documentos[indice_treino])

	#resultado = classificador_svm.predict(X_teste)
	#print(resultado)

	#knn
	classificador_knn = KNeighborsClassifier(n_neighbors = 3)
	classificador_knn.fit(X_treino, Y_treino)
	
	#resultado = classificador_knn.predict(X_teste)
	#print(resultado)


	#resultados
	print('Score SVM e KNN: ')
	print(f'SVM: {classificador_svm.score(X_teste, Y_teste)}')	
	print(f'KNN: {classificador_knn.score(X_teste, Y_teste)}')	

	print('F1 SVM e KNN: ')
	print(f"SVM: {metrics.f1_score(Y_teste, classificador_svm.predict(X_teste), average = 'macro')}")	
	print(f"KNN: {metrics.f1_score(Y_teste, classificador_knn.predict(X_teste), average = 'macro')}")	
	#print(metrics.f1_score(Y_teste, classificador_svm.predict(X_teste), average = 'macro'))
	#print(metrics.f1_score(Y_teste, classificador_knn.predict(X_teste), average = 'macro'))



