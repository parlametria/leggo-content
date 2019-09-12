Crawler para coleta de centenas de pares de Projeto de Lei e lei final publicada

Instruções:
1. Manter junto ao diretório do arquivo fonte o arquivo de paginação por anos (contendo os anos dos quais deseja realizar a coleta)
2. Executar o código no terminal com o formato `python3 crawler_pares.py local1 local2 local3`, sendo os locais os diretórios para se salvar: local1 -> fontes originárias; local2 -> textos finais publicados; local3 -> textos iniciais 
	1. Caso seja desejado reiniciar o código sempre que houver um erro é recomendado rodar no terminal utilizando o formato `until python3 crawler_pares.py local1 local2 local3; do sleep 2; done` que reinicia automaticamente o crawler após dois segundos, se houver alguma falha, enquanto ele não terminar a tarefa (útil para problemas quase intratáveis, como limite de tempo no servidor, lentidão inesperada, erros de carregamento e etc.)


Observações:
* Os locais para se salvar os dados podem ser o mesmo
* Serão gerados dois arquivos, relatorio.txt (com o nome do documento atual e links associados) e log.txt (com um relatório de erros/falhas -por motivo de ausência de dados no site da Câmara- ao tentar coletar arquivos)
