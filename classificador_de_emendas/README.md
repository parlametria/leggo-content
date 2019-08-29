O módulo `ClassificadorDeEmendas` possui 3 funções principais para:
1) criar DataFrame de treino
2) treinar/gerar um modelo SVM
3) utilizar o modelo para classificar blocos de textos de emendas em Aditiva (ADD), Supressiva (SUP), Modificativa (MOD) e nenhuma (O).

Este módulo foi gerado a partir do notebook python `guia_classificador.ipynb`, que se encontra nesta pasta, possui informações de avaliação do modelo e pode ser utilizado como referência.


Abaixo, alguns exemplos de códigos para utilização do módulo:

```
import ClassificadorDeEmendas as clfe
```

Leitura dos Dados
```
emendas = clfe.cria_df_treino("./dados/tagFiles")
```

Criação do Modelo
```
clf = clfe.cria_modelo(emendas)
```

Exemplo de predição
```
print(clfe.preve_emenda("./dados/blocos"))
Gera a saída:
['O' 'SUP']
```
