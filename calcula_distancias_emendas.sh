#!/bin/bash

# Prints message with delimiters.
pretty_print() {
    printf "\n=========================================\n$1\n=========================================\n"
}

# Prints script usage
print_usage() {
    printf "Chamada Correta: calcula_distancias_emendas.sh <REPOS_BASE_PATH> <DATA_DIR_PATH> <ANACONDA_PATH> <ANACONDA_ENV_NAME>"
}

if [ "$#" -lt 4 ]; then
  echo "Número incorreto de parâmetros!"
  print_usage
  exit 1
fi

REPOS_BASE_PATH=$1
DATA_DIR_PATH=$2
ANACONDA_PATH=$3
ANACONDA_ENV_NAME=$4

pretty_print "Iniciando atualização"
# Registra a data de início
date

LEGGO_R_REPO_PATH=$REPOS_BASE_PATH/leggoR/
LEGGO_BACKEND_REPO_PATH=$REPOS_BASE_PATH/leggo-backend/
LEGGO_CONTENT_REPO_PATH=$REPOS_BASE_PATH/leggo-content/
VERSOES_PROPOSICOES_REPO_PATH=$REPOS_BASE_PATH/versoes-de-proposicoes/

pretty_print "Ativando ambiente anaconda"
source $ANACONDA_PATH/bin/activate $ANACONDA_ENV_NAME

pretty_print "Limpando as pastas antes de iniciar o pipeline"	
rm -rf $DATA_DIR_PATH/documentos $DATA_DIR_PATH/documentos_sem_justificacoes/ 
sudo rm $DATA_DIR_PATH/novas_emendas.csv $DATA_DIR_PATH/avulsos_iniciais.csv $DATA_DIR_PATH/textos.csv

pretty_print "Gerando a tabela com os links \npara os arquivos dos textos e emendas"
cd $VERSOES_PROPOSICOES_REPO_PATH
sudo docker-compose run --rm versoes_props Rscript fetcher.R -o data/emendas_raw_old.csv -e data/emendas_raw.csv -n data/novas_emendas.csv -a data/avulsos_iniciais.csv -t data/textos.csv -f 1 

pretty_print "Copiando arquivos do volume para a vm"
api_container_id=$(sudo docker ps | grep servidor-csvs | cut -f 1 -d ' ')
sudo docker cp $api_container_id:agora-digital/exported/novas_emendas.csv $DATA_DIR_PATH
sudo docker cp $api_container_id:agora-digital/exported/avulsos_iniciais.csv $DATA_DIR_PATH
sudo docker cp $api_container_id:agora-digital/exported/textos.csv $DATA_DIR_PATH

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
    $LEGGO_CONTENT_REPO_PATH/util/data/calibre_convert.sh $DATA_DIR_PATH/documentos $DATA_DIR_PATH/log-arquivos-sem-texto.txt

pretty_print "Separando Justificações"
    #Pasta com as emendas e respectivos inteiro teor de cada lei
    DIR_DATA=$DATA_DIR_PATH/documentos

    for folder in $(ls $DIR_DATA/); do
            echo $DIR_DATA/$folder/txt
            python3 $LEGGO_CONTENT_REPO_PATH/util/tools/SepararJustificacoes.py $DIR_DATA/$folder/txt $DATA_DIR_PATH/documentos_sem_justificacoes/ $DATA_DIR_PATH/log-arquivos-sem-texto.txt
    done

    mkdir -p $DATA_DIR_PATH/emendas_all_dist

pretty_print "Calculando as distâncias entre as emendas \ne seus respectivos inteiros teores"
    EMENDAS_FOLDERPATH=$DATA_DIR_PATH/documentos_sem_justificacoes/

    #Baixa stopwords atualizadas
    python3 -c "from nltk import download;download('stopwords')"

    for folder in $(ls $EMENDAS_FOLDERPATH/); do
        python3 $LEGGO_CONTENT_REPO_PATH/coherence/inter_emd_int/inter_emd_int.py $EMENDAS_FOLDERPATH/$folder $LEGGO_CONTENT_REPO_PATH/coherence/languagemodel/vectors_skipgram_lei_aprovadas.bin $DATA_DIR_PATH/emendas_all_dist/
    done

pretty_print "Adicionando a coluna distancia na tabela \nde emendas do back"
    cd $LEGGO_R_REPO_PATH

    #Verifica se há distâncias
    if [ $(ls $DATA_DIR_PATH/emendas_all_dist/ | wc -l) -eq 0 ]
    then
        echo "Não há novas distâncias"
        exit 0
    else
       api_container_id=$(sudo docker ps | grep servidor-csvs | cut -f 1 -d ' ')
       sudo docker cp $DATA_DIR_PATH/emendas_all_dist/. $api_container_id:agora-digital/exported/emendas_with_distances
       sudo docker-compose run --rm rmod \
       Rscript scripts/update_emendas_dist.R \
       exported/emendas_with_distances \
       data/distancias/ \
       exported/emendas_raw.csv \
       exported/emendas.csv    
    fi
fi
