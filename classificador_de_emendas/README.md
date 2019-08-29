O módulo `ClassificadorDeEmendas` possui 3 funções principais para:
1) criar DataFrame de treino
2) treinar/gerar um modelo SVM
3) utilizar o modelo para classificar blocos de textos de emendas em Aditiva (ADD), Supressiva (SUP), Modificativa (MOD) e nenhuma (O).

Este módulo foi gerado a partir do notebook python `guia_classificador.ipynb`, que se encontra nesta pasta. Este arquivo possui informações de avaliação do modelo (acurácia, matriz de confusão), gera os resultados em `data/results/modelo_classificador_de_emendas/` e pode ser utilizado como referência.


Abaixo, alguns exemplos de códigos para utilização do módulo:

```
import ClassificadorDeEmendas as clfe
```

Leitura dos Dados
```
emendas = clfe.cria_df_treino("../data/tag_files")
```

Criação do Modelo `emend_clf_pipe` no mesmo diretório
```
clf = clfe.cria_modelo(emendas)
```

Exemplo de predição. Carrega o modelo `emend_clf_pipe` que está no mesmo diretório. Como entrada, pode ser qualquer diretório de `data/blocos/`.
```
print(clfe.preve_emenda("../data/blocos/exemplo_2_blocos"))
Gera a saída:
['O' 'SUP']
```
