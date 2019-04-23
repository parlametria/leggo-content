Algumas ferramentas úteis para baixar, converter e processar dados.

## Script para download de pdf's
O script download_csv_prop.py demanda dois argumentos na linha de comando para ser executado, como no esquema a seguir:

python download_csv_prop.py ARQUIVO_CSV_COM_LINKS DIRETORIO_SAIDA

O argumento ARQUIVO_CSV_COM_LINKS deve ser um arquivo csv com cabeçalho, o qual deve conter  ao menos os seguintes campos: "link_inteiro_teor", 
"id_proposicao" e "codigo_texto". 

O argumento DIRETORIO_SAIDA será o diretório onde os pdf's das urls serão baixados. Dado o próximo script a ser executado ser calibre_convert.sh (próxima sessão), é recomendado baixar em um diretório com a seguinte estrutura DIRETORIO_SAIDA/pdf/.

## Script para conversão de pdf's para txt's

O script calibre_convert.sh, converte documentos pdf em documentos txt. Para funcionar, é necessário instalar o programa Calibre (https://calibre-ebook.com/). Para utilizar o script executa-se em um terminar bash o seguinte comando:

$ ./calibre_convert.sh DIRETORIO_DE_DADOS

O script assume que DIRETORIO_DE_DADOS possui um subdiretorio chamado pdf, onde estão os pdf's a serem convertidos, e também assumindo que DIRETORIO_DE_DADOS possui um subdiretório txt, para onde vai a saída dos arquivos convertidos. 

Arquivos pdf's que foram digitalizados como imagens não conseguem ser convertidos pelo Calibre, portanto é importante que a saída seja 
verificada.

