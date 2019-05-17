Segmentador de Emendas

As emendas à PLs possuem uma estrutura que consiste, no geral, em uma introdução seguida de pares de anúncio do que será feito (emenda substitutiva/modificativa, aditiva ou supressiva) e a alteração em si. A ideia é segmentar o texto dessas emendas de forma que todas essas partes fiquem separadas.
Para isso foi utilizado uma abordagem supervisionada com o modelo de Conditional Random Fields (CRF), que tem como entrada uma lista de features (para cada segmento) e uma tag que identifica o tipo de segmento.
As features são construídas a partir de cada palavra no segmento e as utilizadas (no momento) são:
	* A palavra em minúsculo
	* Se a palavra está em maiúsculo (booleano)
	* Se a palavra é um título (booleano)
	* Se a palavra é um dígito (booleano)
	* POS-Tag da palavra
	* E todas estas mesmas features para a palavra anterior e posterior, se houver (criação de contexto)
