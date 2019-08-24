Arquivos para processamento de segmentos.
Adequa os segmentos de forma que a ligação com o objeto de compilador de leis fique fácil.

Instruções:
1. Rodar o comando "python3 parser_itens.py local1", sendo local1 o diretório onde os arquivos de texto se encontram. Este programa extrai os itens de lei e os enumera.
2. Rodar o comando "python3 agregador.py local1", sendo local1 o diretório onde os arquivos de texto, agora processados pelo parser_itens.py, se encontram. Este programa busca agregar os itens de lei (por exemplo, saber de qual artigo faz parte um parágrafo extraído do programa anterior), de forma heurística.

Observação: O programa irá adicionar (fazer um append) dos termos de interesse (artigo, inciso, parágrafo, alínea) e destes próprios termos de forma agregada nos próprios arquivos, portanto recomenda-se utilizar uma cópia da pasta dos arquivos de texto pois o conteúdo original será adicionado dos termos extraídos. Cada arquivo na pasta será alterado e terá os seguintes conteúdos:
	1. Texto original presente no arquivo
	2. Itens de lei extraídos e enumerados, contidos entre os marcadores "!@#$%" e "%$#@!"
	3. Itens de lei agregados, contidos entre os marcadores "__INICIO_AGREGADOR__" e "__FIM_AGREGADOR__"
