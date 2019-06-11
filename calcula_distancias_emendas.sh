#!/bin/bash

# Prints message with delimiters.
pretty_print() {
    printf "\n===============================\n$1\n===============================\n"
}

# Prints script usage
print_usage() {
    printf "Chamada Correta: calcula_distancias_emendas.sh <LEGGO_R_REPO_PATH> <LEGGO_BACKEND_REPO_PATH> <LEGGO_CONTENT_REPO_PATH> <VERSOES_PROPOSICOES_REPO_PATH> <DATA_DIR_PATH>"
}

if [ "$#" -lt 5 ]; then
  echo "Número errado de parâmetros!"
  print_usage
  exit 1
fi

LEGGO_R_REPO_PATH=$1
LEGGO_BACKEND_REPO_PATH=$2
LEGGO_CONTENT_REPO_PATH=$3
VERSOES_PROPOSICOES_REPO_PATH=$4
DATA_DIR_PATH=$5

cd $VERSOES_PROPOSICOES_REPO_PATH

pretty_print "Gerando a tabela com os links para os arquivos dos textos e emendas"
Rscript $VERSOES_PROPOSICOES_REPO_PATH/fetcher.R -i $LEGGO_R_REPO_PATH/data/tabela_geral_ids_casa.csv -e $LEGGO_BACKEND_REPO_PATH/data/emendas_raw.csv -o $DATA_DIR_PATH/novas_emendas.csv -a $DATA_DIR_PATH/avulsos_iniciais.csv

pretty_print "Verificando se há novas emendas"
if [ $(cat $DATA_DIR_PATH/novas_emendas.csv | wc -l) -lt 2 ]
then
    echo "Não há novas emendas"
    exit 0
else
    mkdir -p $DATA_DIR_PATH/documentos

pretty_print "Baixando os arquivos em pdf"
    python3 $LEGGO_CONTENT_REPO_PATH/util/data/download_csv_prop.py $DATA_DIR_PATH/novas_emendas.csv $DATA_DIR_PATH/documentos/ 
    python3 $LEGGO_CONTENT_REPO_PATH/util/data/download_csv_prop.py $DATA_DIR_PATH/avulsos_iniciais.csv $DATA_DIR_PATH/documentos/ 

pretty_print "Convertendo de pdf para txt"
    $LEGGO_CONTENT_REPO_PATH/util/data/calibre_convert.sh $DATA_DIR_PATH/documentos $DATA_DIR_PATH/documentos/log-arquivos-sem-texto.txt

pretty_print "Separando Justificações"
    #Pasta com as emendas e respectivos inteiro teor de cada lei
    DIR_DATA=$DATA_DIR_PATH/documentos

    for folder in $(ls $DIR_DATA/); do
            echo $DIR_DATA/$folder/txt
            python3 $LEGGO_CONTENT_REPO_PATH/util/tools/SepararJustificacoes.py $DIR_DATA/$folder/txt $DATA_DIR_PATH/documentos_sem_justificacoes/
    done

    mkdir -p $DATA_DIR_PATH/emendas_all_dist

pretty_print "Calculando as distâncias entre as emendas e seus respectivos inteiros teores"
    EMENDAS_FOLDERPATH=$DATA_DIR_PATH/documentos_sem_justificacoes/

    #Baixa stopwords atualizadas
    python3 -c "from nltk import download;download('stopwords')"

    for folder in $(ls $EMENDAS_FOLDERPATH/); do
        python3 $LEGGO_CONTENT_REPO_PATH/coherence/inter_emd_int/inter_emd_int.py $EMENDAS_FOLDERPATH/$folder $LEGGO_CONTENT_REPO_PATH/coherence/languagemodel/vectors_skipgram_lei_aprovadas.bin $DATA_DIR_PATH/emendas_all_dist/
    done

pretty_print "Adicionando a coluna distancia a tabela de emendas do back"
    #Instalar versão mais recente do código R
    cd $LEGGO_R_REPO_PATH; git pull; Rscript -e "devtools::install()"

    #Verifica se há distâncias
    if [ $(ls $DATA_DIR_PATH/emendas_all_dist/ | wc -l) -eq 0 ]
    then
        echo "Não há novas distâncias"
        exit 0
    else
        Rscript $LEGGO_R_REPO_PATH/scripts/update_emendas_dist.R $DATA_DIR_PATH/emendas_all_dist/ $LEGGO_R_REPO_PATH/data/distancias/ $LEGGO_BACKEND_REPO_PATH/data/emendas_raw.csv $LEGGO_BACKEND_REPO_PATH/data/emendas.csv 
    fi
fi
