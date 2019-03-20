# Documentação
A documentação trata do uso do script **inter_coherence.py**! 
O script realiza a comparação NxN de arquivos em um diretório usando o WMD


# Uso

O uso do script é muito simples. Necessitando apenas de alguns pré requisitos

### Pre requisitos python:
* nltk 
* gensim
* pandas
* numpy


## Rodando o script

O script recebe três argumentos:
* O Path para pasta onde estão os textos/PLs extraídas
* O Path para o arquivo .bin do modelo Word2Vec treinado
* O Path para a pasta onde a tabela de features deve ser salva

## Exemplo de uso

    python inter_coherence.py /Users/local/originals /User/local/model/model.bin /User/local/features
