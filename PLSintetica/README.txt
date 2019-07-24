A estrutura criada pelo script plObjFunc.py é baseada na estrutura hierárquica de uma lei, projeto de lei ou PEC.
A hierarquia do texto de uma lei consite, do nível mais alto para o mais baixo, artigo, parágrafo, inciso e alínea.

No plObj, cada nível hierárquico é pensado como um objeto que é definido como uma lista, essa lista contém dois itens que são:
	- O texto do nível atual;
	- Uma lista que contém os objetos do nível abaixo;
	
Ou seja, um parágrafo é composto por uma lista que contém em seu índice 0 a string com seu texto e em seu índice 1 uma lista com os objetos de nível inferior.

Para o correto funcionamento do script deve-se garantir que cada nível (artigo, parágrafo, alínea e inciso) esteja em início de linha e precedido por uma quebra de linha, pois 
as expressões regulares utilizadas buscam a quebra de linha. Isso foi deinido com a intenção de diferenciar os níveis do texto processado de menções a outros 
textos de lei. Veja um exemplo do Art. 3 da MPV 870:

Art. 3º À Casa Civil da Presidência da República compete:

I - assistir diretamente o Presidente da República no desempenho de suas atribuições, especialmente:

a) na coordenação e na integração das ações governamentais;

b) na verificação prévia da constitucionalidade e da legalidade dos atos presidenciais;

c) na análise do mérito, da oportunidade e da compatibilidade das propostas, inclusive das matérias em tramitação no Congresso Nacional, com as diretrizes governamentais;

d) na avaliação e no monitoramento da ação governamental e da gestão dos órgãos e das entidades da administração pública federal;

e) na coordenação política do Governo federal; e

f) na condução do relacionamento do Governo federal com o Congresso Nacional e com os partidos políticos; e

II - publicar e preservar os atos oficiais.


