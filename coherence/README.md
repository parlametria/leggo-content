Neste diretório se encontram o código para cálculo da coerência e datasets utlizados para tais cálculos.

## Dataset 

O dataset é composto atualmente por dois projetos de lei, a saber, 10 medidas contra a corrupção e Moro. Junto dessas existem também pareceres relacionados. 

A organização de projetos de lei em seu texto original segue a seguinte estrutura:

1st. Artigos

	1 - Parágrafos

		I. Subseções

			a. Alíneas


Para gerar o arquivo de texto cru do conjunto de dados, cada seção hierarquicamente superior é concatenada com a seção 
hierarquicamente inferior. Por exemplo, em um artigo com o formato a seguir:

1st. Esta lei lida com:

	1 - Os problemas de lidar com:

		I. Contextos longos

			a. No caso de uma arquitetura LSTM

			b. No caso de uma arquitetura CNN

		II. Sentenças longas

			a. No caso de uma arquitetura word2vec

			b. No caso de comparações wmd.

Vira os seguintes itens no arquico de texto cru:

(1) Esta lei lida com: Os problema de lidar com: Contextos longos no caso de uma arquitetura LSTM.

(2) Esta lei lida com: Os problema de lidar com: Contextos longos no caso de uma arquitetura CNN.

(3) Esta lei lida com: Os problema de lidar com: Sentenças longas no caso de uma arquitetura word2vec.

(4) Esta lei lida com: Os problema de lidar com: Sentenças longas no caso de comparações wmd.

Cada item desse é definido como uma *linha* dentro do arquivo de texto cru, cujo nome do arquivo é o nome da PL. 



Fonte: https://github.com/analytics-ufcg/leggo-content/blob/master/artigos/NLP_Article.pdf



