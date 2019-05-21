import nltk
import string


#tokenização
def tokeniza(documento):
	tokens = nltk.word_tokenize(documento)
	return tokens


#remoção de stopwords
def remove_stopwords(tokens):
	stop_words_pt = nltk.corpus.stopwords.words('portuguese')
	for token in tokens:
		if token in stop_words_pt:
			tokens = list(filter(lambda p: p != token, tokens))

	return tokens


#remoção de palavras muito ou pouco frequentes
def remove_extremos_de_frequencia(texto, tokens):
	mapa_frequencias = {} #dicionario contendo apenas as palavras tokenizadas
	for palavra in tokens:
		mapa_frequencias[palavra] = 1

	for palavra in texto.split():
		if palavra in mapa_frequencias:
			mapa_frequencias[palavra] += 1

	mapa_frequencias = dict(sorted(mapa_frequencias.items(), key = lambda item: item[1], reverse = True))
	

	for palavra in mapa_frequencias.keys():
		if palavra in tokens:
			if mapa_frequencias[palavra] == 1 or mapa_frequencias[palavra] == 2: #remove menos frequentes
				tokens = list(filter(lambda p: p != palavra, tokens))

	for palavra in list(mapa_frequencias.keys())[:10]: #remove as 10 mais frequentes
		if palavra in tokens:
			tokens = list(filter(lambda p: p != palavra, tokens))

	return tokens


### main
def main():
	with open('texto_de_teste.txt', 'r') as arquivo:
		texto = arquivo.read()

	#colocando em minúsculo e removendo pontuação
	texto = ' '.join(palavra.strip(string.punctuation) for palavra in texto.lower().split())

	#tokenizando 
	tokens = tokeniza(texto)

	#removendo stopwords
	tokens = remove_stopwords(tokens)

	#removendo palavras mais e menos frequentes
	tokens = remove_extremos_de_frequencia(texto, tokens)

	print(tokens)

	

if __name__ == "__main__":
	main()

