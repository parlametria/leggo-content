import pycrfsuite
from sklearn.model_selection import train_test_split

def leitura_de_dados(arquivo_de_entrada):
	with open(arquivo_de_entrada, 'r') as arquivo:
		linhas = arquivo.readlines()

	pares_palavra_tag = []
	for linha in linhas:
		tupla = tuple(linha.split())
		#print(tupla)
		pares_palavra_tag.append(tupla)

	return pares_palavra_tag


def separa_em_blocos(pares_palavra_tag):
	documentos = [] 
	documento = []
	for i in range(len(pares_palavra_tag)):
		documento.append(pares_palavra_tag[i])
		if('E' in pares_palavra_tag[i][1]):
			documentos.append(documento)
			documento = []

	return documentos


def criador_de_features(documento, posicao_do_par):
	palavra = documento[posicao_do_par][0]
	tag = documento[posicao_do_par][1]

	features = [ 
		'bias',
		'palavra_minusculo=' + palavra.lower(),
		'esta_em_maiusculo=%s' % palavra.isupper(),
		'e_titulo=%s' % palavra.istitle(),
		'e_digito=%s' % palavra.isdigit()
	] #features genéricas, servem para qualquer palavra no documento/bloco, independentemente de sua posição

	#aqui podem ser acrescentadas features dependendo da posição da palavra no documento/bloco
	#por exemplo, palavras que estão entre as primeira e última palavras do bloco podem tomar como features as palavras ao redor

	return features


def main():
	pares_palavra_tag = leitura_de_dados('exemplo_entrada.txt')

	pares_com_O = [tupla for tupla in pares_palavra_tag if tupla[1] == 'O'] #pares apenas com out of segment
	pares_palavra_tag = [tupla for tupla in pares_palavra_tag if tupla[1] != 'O'] #pares apenas com segmentos com conteúdo informativo
	
	documentos = separa_em_blocos(pares_palavra_tag) #cada segmento é um documento, as tags B e E indicam o início e o fim de um segmento
	
	#print(documentos[0][0])
	#print(criador_de_features(documentos[0], 0))

	X = [] #vetor de features, cada posição contém as features de uma palavra
	for documento in documentos:
		for i in range(len(documento)):
			X.append(criador_de_features(documento, i))

	y = []
	for par in pares_palavra_tag:
		y.append(par[1])

	#print(len(X))
	#print(len(y))
	#print(len(pares_com_O))
	#print(X[0])
	#print(y[0])

	X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size = 0.2)

	modelo = pycrfsuite.Trainer(verbose = True)

	for unidade_x, unidade_y in zip(X_treino, y_treino):
		modelo.append(unidade_x, unidade_y)

	modelo.set_params({
		'c1': 0.1,
		'c2': 0.01,
		'max_iterations': 100,
		'feature.possible_transitions': True
	})

	modelo.train('modelo.model')
	

if __name__ == "__main__":
	main()
