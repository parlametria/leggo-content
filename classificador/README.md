classificador_kfold.py
	Instruções:
		1. Certifique-se que as bibliotecas numpy, nltk e scikit-learn estão instaladas
		2. Coloque o arquivo preprocessamento.py no mesmo diretório
		3. Na função leitura_dados() coloque o caminho para o arquivos que tem os nomes das PLs com suas categorias e para o diretório com os textos iniciais de cada PL, respectivamente, como indicado no código
		4. Execute com "python3 classificador_kfold.py"
	Saída:
		Saída com print na tela. Acurácias totais e por classe dos modelos SVM e KNN com os parâmetros setados.


classificador_grid_search.py
	Instruções:
		1. Certifique-se que as bibliotecas numpy, nltk e scikit-learn estão instaladas
		2. Coloque o arquivo preprocessamento.py no mesmo diretório
		3. Na função leitura_dados() coloque o caminho para o arquivos que tem os nomes das PLs com suas categorias e para o diretório com os textos iniciais de cada PL, respectivamente, como indicado no código
		5. Na main(), defina os valores dos parâmetros os quais deseja testar (alguns já estão definidos) logo antes das funções que fazem os grid searches serem chamadas
		4. Execute com "python3 classificador_grid_search.py"
	Saída:
		Saída escrita em dois arquivos. Melhores parâmetros encontrados para os modelos SVM e KNN.
