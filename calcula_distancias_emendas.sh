#!/bin/bash

# Prints message with delimiters.
pretty_print() {
    printf "\n=========================================\n$1\n=========================================\n"
}

# Prints script usage
print_usage() {
    printf "Chamada Correta: calcula_distancias_emendas.sh <REPOS_BASE_PATH> <DATA_DIR_PATH>"
}

if [ "$#" -lt 2 ]; then
  echo "Número errado de parâmetros!"
  print_usage
  exit 1
fi

REPOS_BASE_PATH=$1
DATA_DIR_PATH=$2

LEGGO_R_REPO_PATH=$REPOS_BASE_PATH/leggoR/
LEGGO_BACKEND_REPO_PATH=$REPOS_BASE_PATH/leggo-backend/
LEGGO_CONTENT_REPO_PATH=$REPOS_BASE_PATH/leggo-content/
VERSOES_PROPOSICOES_REPO_PATH=$REPOS_BASE_PATH/versoes-de-proposicoes/

pretty_print "Limpando as pastas antes de iniciar o pipeline"	
rm -rf $DATA_DIR_PATH/documentos $DATA_DIR_PATH/documentos_sem_justificacoes/ 

pretty_print "Copiando arquivos do volume para a vm"
api_container_id=$(sudo docker ps | grep back_api | cut -f 1 -d ' ')
sudo docker cp $api_container_id:agora-digital-backend/data/emendas_raw.csv $DATA_DIR_PATH
sudo docker cp $api_container_id:agora-digital-backend/data/emendas_raw_old.csv $DATA_DIR_PATH

pretty_print "Gerando a tabela com os links \npara os arquivos dos textos e emendas"
cd $VERSOES_PROPOSICOES_REPO_PATH
Rscript $VERSOES_PROPOSICOES_REPO_PATH/fetcher.R -o $DATA_DIR_PATH/emendas_raw_old.csv -e $DATA_DIR_PATH/emendas_raw.csv -n $DATA_DIR_PATH/novas_emendas.csv -a $DATA_DIR_PATH/avulsos_iniciais.csv -t $DATA_DIR_PATH/textos.csv -f 1 

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
    echo "Instalando versão mais recente do código leggoR..."
    cd $LEGGO_R_REPO_PATH; git pull; sudo docker-compose build

    #Verifica se há distâncias
    if [ $(ls $DATA_DIR_PATH/emendas_all_dist/ | wc -l) -eq 0 ]
    then
        echo "Não há novas distâncias"
        exit 0
    else
       api_container_id=$(sudo docker ps | grep back_api | cut -f 1 -d ' ')
       sudo docker cp $DATA_DIR_PATH/emendas_all_dist/. $api_container_id:agora-digital-backend/data/emendas_with_distances
       sudo docker-compose run --rm rmod \
       Rscript scripts/update_emendas_dist.R \
       exported/emendas_with_distances \
       data/distancias/ \
       exported/emendas_raw.csv \
       exported/emendas.csv    

       pretty_print "Inserindo novos dados de emendas no Backend."
       sudo docker exec $api_container_id sh -c './manage.py flush --no-input; ./manage.py import_data'
    fi
fi
