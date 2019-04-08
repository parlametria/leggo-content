#formatação de labels
import numpy as np

#pré-processamento dos textos das PLs
from preprocessamento import tokenizador #tokenizador próprio

#embedding TF-IDF
#from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

#treinos
from sklearn.model_selection import KFold
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


def treino_svm_e_knn(dicionario_categorias, X, Y):
	'''
	Realiza os treinos dos modelos SVM e KNN
	Retorno: números relativos à acurácia total e por classe de cada modelo
	'''

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
		print('em treino...')
		X_treino, X_teste = X[indice_treino], X[indice_teste]
		Y_treino, Y_teste = Y[indice_treino], Y[indice_teste]

		vetorizador = TfidfVectorizer(analyzer = 'word', tokenizer = tokenizador) #tokenizador próprio
		#vetorizador = TfidfVectorizer()
		vetorizador.fit(X_treino)
		X_treino = vetorizador.transform(X_treino)
		X_teste = vetorizador.transform(X_teste)
		#print(X_treino[0].shape)
		#exit(0)

		#svm
		classificador_svm = svm.SVC(gamma = 'auto', decision_function_shape = 'ovo', C = 1000, kernel = 'linear')
		classificador_svm.fit(X_treino, Y_treino)
		pred_svm = classificador_svm.predict(X_teste)
		acuracia_media_svm = 0.0
		for i in range(0, len(pred_svm)):
			if(pred_svm[i] == Y_teste[i]):
				acertos_por_classe_svm[pred_svm[i]] += 1.0
				acuracia_media_svm += 1.0
			else:
				erros_por_classe_svm[pred_svm[i]] += 1.0
		acuracia_svm += acuracia_media_svm / len(pred_svm)

	
		#knn
		classificador_knn = KNeighborsClassifier(n_neighbors = 5, weights = 'distance', p = 1, metric = 'cosine')
		classificador_knn.fit(X_treino, Y_treino)
		pred_knn = classificador_knn.predict(X_teste)
		acuracia_media_knn = 0.0
		for i in range(0, len(pred_knn)):
			if(pred_knn[i] == Y_teste[i]):
				acertos_por_classe_knn[pred_knn[i]] += 1.0
				acuracia_media_knn += 1.0
			else:
				erros_por_classe_knn[pred_knn[i]] += 1.0
		acuracia_knn += acuracia_media_knn / len(pred_knn)

	return acuracia_svm, acertos_por_classe_svm, erros_por_classe_svm, acuracia_knn, acertos_por_classe_knn, erros_por_classe_knn


def print_resultados(nome_modelo, dicionario_categorias, acuracia, acertos_por_classe, erros_por_classe):
	'''
	Imprime os resultados
	Retorno: void
	'''

	print('Acurácia total ' + nome_modelo + ': ' + str(acuracia / 5.0))
	print('Acurácias por classe ' + nome_modelo + ':')
	for classe in dicionario_categorias.keys():
		acc_classe_atual = acertos_por_classe[dicionario_categorias[classe]] / (acertos_por_classe[dicionario_categorias[classe]] + erros_por_classe[dicionario_categorias[classe]])
		print(classe + ': ' + str(acc_classe_atual))
	print('\n')



def main():
	################################## leituras
	linhas, lista_textos, dicionario_categorias, nomes_documentos = leitura_dados()


	################################## formatação de labels e dados de treino
	i = 1
	for chave in dicionario_categorias.keys():
		dicionario_categorias[chave] = i #atribuição de valor numérico para cada categoria
		i += 1

	Y = labels_formatadas(dicionario_categorias, linhas) #labels
	X = np.array(lista_textos) #dados


	################################## treinos
	acuracia_svm, acertos_por_classe_svm, erros_por_classe_svm, acuracia_knn, acertos_por_classe_knn, erros_por_classe_knn = treino_svm_e_knn(dicionario_categorias, X, Y)


	################################## resultados
	print_resultados('SVM', dicionario_categorias, acuracia_svm, acertos_por_classe_svm, erros_por_classe_svm)
	print_resultados('KNN', dicionario_categorias, acuracia_knn, acertos_por_classe_knn, erros_por_classe_knn)


if __name__ == "__main__":
    main()


