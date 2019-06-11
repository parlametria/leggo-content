#!/bin/bash

#if [ ]
#then
#fi


#VERSOES_PROPOSICOES_REPO_PATH=$1
#LEGGO_CONTENT_REPO_PATH=$2
#LEGGOR_REPO_PATH=$3
#DATA_DIR_PATH=$4

cd ../versoes-de-proposicoes/
#Gera a tabela com os links para os arquivos dos textos e emendas
Rscript fetcher.R -i ../leggoR/data/tabela_geral_ids_casa.csv -e ../leggo-backend/data/emendas_raw.csv -o novas_emendas.csv -a avulsos_iniciais.csv

#Verifica se há novas emendas
if [ $(cat novas_emendas.csv | wc -l) -lt 2 ]
then
    echo "Não há novas emendas"
    exit 0
else
    mkdir -p documentos

    #Entra na pasta data do leggo-content
    cd ../leggo-content/util/data/

    #Download dos arquivos em pdf
    python3 download_csv_prop.py ../../../versoes-de-proposicoes/novas_emendas.csv ../../../versoes-de-proposicoes/documentos/ 
    python3 download_csv_prop.py ../../../versoes-de-proposicoes/avulsos_iniciais.csv ../../../versoes-de-proposicoes/documentos/ 

    #Converte de pdf para txt
    ./calibre_convert.sh ../../../versoes-de-proposicoes/documentos log-arquivos-sem-texto.txt

    #Separa Justificacoes
    #Pasta com as emendas e respectivos inteiro teor de cada lei
    DIR_DATA="../../../versoes-de-proposicoes/documentos"

    for folder in $(ls $DIR_DATA/); do
            echo $DIR_DATA/$folder/txt
            python3 ../tools/SepararJustificacoes.py $DIR_DATA/$folder/txt ./documentos_sem_justificacoes/
    done

    mkdir -p emendas_all_dist

    #Calcula todas as distancias para todas as props
    EMENDAS_FOLDERPATH="./documentos_sem_justificacoes/"

    #Baixa stopwords atualizadas
    python3 -c "from nltk import download;download('stopwords')"

    #Calcula distâncias entre as emendas e seus respectivos inteiros teores
    for folder in $(ls $EMENDAS_FOLDERPATH/); do
        python3 ../../coherence/inter_emd_int/inter_emd_int.py $EMENDAS_FOLDERPATH$folder ../../coherence/languagemodel/vectors_skipgram_lei_aprovadas.bin emendas_all_dist/
    done

    #Adicionar a coluna distancia a tabela de emendas do back
    cd ../../../leggoR

    #Verifica se há distâncias
    if [ $(ls ../leggo-content/util/data/emendas_all_dist/ | wc -l) -eq 0 ]
    then
        echo "Não há novas distâncias"
        exit 0
    else
        Rscript scripts/update_emendas_dist.R ../leggo-content/util/data/emendas_all_dist/ data/distancias/ ../leggo-backend/data/emendas_raw.csv ../leggo-backend/data/emendas.csv 
    fi
fi







