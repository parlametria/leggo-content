#formatação
import numpy as np
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


################################## treinos
X = np.array(lista_textos)
kf_5 = KFold(n_splits = 5, shuffle = True)
acuracia_svm = 0.0
acuracia_knn = 0.0
acertos_por_classe_svm = {}
erros_por_classe_svm = {}
acertos_por_classe_knn = {}
erros_por_classe_knn = {}
for classe in dicionario_categorias.values():
	acertos_por_classe_svm[classe] = 0.0
	acertos_por_classe_knn[classe] = 0.0
	erros_por_classe_knn[classe] = 0.0
	erros_por_classe_svm[classe] = 0.0

for indice_treino, indice_teste in kf_5.split(X):
	X_treino, X_teste = X[indice_treino], X[indice_teste]
	Y_treino, Y_teste = Y[indice_treino], Y[indice_teste]

	vetorizador = TfidfVectorizer()
	vetorizador.fit(X_treino)
	X_treino = vetorizador.transform(X_treino)
	X_teste = vetorizador.transform(X_teste)


	#svm
	classificador_svm = svm.SVC(gamma = 'auto', decision_function_shape = 'ovo', C = 1000, kernel = 'linear')
	classificador_svm.fit(X_treino, Y_treino)
	pred_svm = classificador_svm.predict(X_teste)
	for i in range(0, len(pred_svm)):
		if(pred_svm[i] == Y_teste[i]):
			acertos_por_classe_svm[pred_svm[i]] += 1.0
		else:
			erros_por_classe_svm[pred_svm[i]] += 1.0

	#knn
	classificador_knn = KNeighborsClassifier(n_neighbors = 5, weights = 'distance', p = 1)
	classificador_knn.fit(X_treino, Y_treino)
	pred_knn = classificador_knn.predict(X_teste)
	for i in range(0, len(pred_knn)):
		if(pred_knn[i] == Y_teste[i]):
			acertos_por_classe_knn[pred_knn[i]] += 1.0
		else:
			erros_por_classe_knn[pred_knn[i]] += 1.0

print('Acurácias por classe SVM:')
for classe in dicionario_categorias.keys():
	acc_classe_atual = acertos_por_classe_svm[dicionario_categorias[classe]] / (acertos_por_classe_svm[dicionario_categorias[classe]] + erros_por_classe_svm[dicionario_categorias[classe]])
	print(classe + ': ' + str(acc_classe_atual))

print('Acurácias por classe KNN:')
for classe in dicionario_categorias.keys():
	acc_classe_atual = acertos_por_classe_knn[dicionario_categorias[classe]] / (acertos_por_classe_knn[dicionario_categorias[classe]] + erros_por_classe_knn[dicionario_categorias[classe]])
	print(classe + ': ' + str(acc_classe_atual))


	'''
	#resultados
	print('Score SVM e KNN: ')
	print(f'SVM: {classificador_svm.score(X_teste, Y_teste)}')	
	print(f'KNN: {classificador_knn.score(X_teste, Y_teste)}')	

	print('F1 SVM e KNN: ')
	print(f"SVM: {metrics.f1_score(Y_teste, classificador_svm.predict(X_teste), average = 'macro')}")	
	print(f"KNN: {metrics.f1_score(Y_teste, classificador_knn.predict(X_teste), average = 'macro')}")
	'''


