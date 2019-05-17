Segmentador de Emendas <br /> <br />

As emendas à PLs possuem uma estrutura que consiste, no geral, em uma introdução seguida de pares de anúncio do que será feito (emenda substitutiva/modificativa, aditiva ou supressiva) e a alteração em si. A ideia é segmentar o texto dessas emendas de forma que todas essas partes fiquem separadas. <br />
Para isso foi utilizado uma abordagem supervisionada com o modelo de Conditional Random Fields (CRF), que tem como entrada uma lista de features (para cada segmento) e uma tag que identifica o tipo de segmento. <br />
As features são construídas a partir de cada palavra no segmento e as utilizadas (no momento) são: <br />
	* A palavra em minúsculo <br />
	* Se a palavra está em maiúsculo (booleano) <br />
	* Se a palavra é um título (booleano) <br />
	* Se a palavra é um dígito (booleano) <br />
	* POS-Tag da palavra <br />
	* E todas estas mesmas features para a palavra anterior e posterior, se houver (criação de contexto) <br />
