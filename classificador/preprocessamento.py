import nltk
import string
import numpy as np

#tokenização
def tokeniza(documento):
	tokenizado = nltk.word_tokenize(documento)

	return tokenizado


#remoção de stopwords
def remove_stopwords(texto_tokenizado):
	stop_words_pt = set(nltk.corpus.stopwords.words('portuguese'))

	texto_tokenizado = list(filter(lambda p: p not in stop_words_pt, texto_tokenizado))



#remoção de palavras muito ou pouco frequentes
def remove_extremos_de_frequencia(texto_tokenizado):
	mapa_frequencias = {token: 0 for token in texto_tokenizado} #dicionario (elementos únicos)

	for palavra in texto_tokenizado:
		mapa_frequencias[palavra] += 1

	texto_tokenizado = list(filter(lambda p: mapa_frequencias[p] > 2, texto_tokenizado)) #deixa apenas palavras com frequência maior que 2
	
	for palavra, _ in sorted(mapa_frequencias.items(), key = lambda item: item[1], reverse = True)[:10]: #remove as 10 mais frequentes
		texto_tokenizado = list(filter(lambda p: p != palavra, texto_tokenizado))

	return texto_tokenizado


#tokenizador central, aplica todas funções e retorna o texto tokenizado
def tokenizador(texto):
	#obtém texto tokenizado 
	texto_tokenizado = tokeniza(texto.lower())

	#removendo stopwords
	texto_tokenizado = remove_stopwords(texto_tokenizado)

	#removendo palavras mais e menos frequentes
	texto_tokenizado = remove_extremos_de_frequencia(texto_tokenizado)

	return np.array(texto_tokenizado) #retorna texto tokenizado, mas não com tokens únicos

