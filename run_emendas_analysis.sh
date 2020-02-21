#!/bin/bash

# Prints message with delimiters.
pretty_print() {
    printf "\n=========================================\n$1\n=========================================\n"
}

# Prints script usage
print_usage() {
    printf "Chamada Correta: run_emendas_analysis.sh <VOLUME_MOUNT_PATH>"
}

if [ "$#" -lt 1 ]; then
  echo "Número incorreto de parâmetros!"
  print_usage
  exit 1
fi

VOLUME_MOUNT_PATH=$1

pretty_print "Iniciando atualização"
# Registra a data de início
date

pretty_print "Limpando as pastas antes de iniciar o pipeline"	
rm -rf $VOLUME_MOUNT_PATH/documentos $VOLUME_MOUNT_PATH/documentos_sem_justificacoes/ 

pretty_print "Verificando se há novas emendas"
if [ $(cat $VOLUME_MOUNT_PATH/novas_emendas.csv | wc -l) -lt 2 ]
then
    echo "Não há novas emendas"
    exit 0
else
    mkdir -p $VOLUME_MOUNT_PATH/documentos

    pretty_print "Baixando os arquivos em pdf"
        python3 util/data/download_csv_prop.py $VOLUME_MOUNT_PATH/novas_emendas.csv $VOLUME_MOUNT_PATH/documentos/ 
        python3 util/data/download_csv_prop.py $VOLUME_MOUNT_PATH/avulsos_iniciais.csv $VOLUME_MOUNT_PATH/documentos/ 

    pretty_print "Convertendo de pdf para txt"
        util/data/calibre_convert.sh $VOLUME_MOUNT_PATH/documentos $VOLUME_MOUNT_PATH/log-arquivos-sem-texto.txt

    pretty_print "Separando Justificações"
    #Pasta com as emendas e respectivos inteiro teor de cada lei
        DIR_DATA=$VOLUME_MOUNT_PATH/documentos

        for folder in $(ls $DIR_DATA/); do
                echo $DIR_DATA/$folder/txt
                python3 util/tools/SepararJustificacoes.py $DIR_DATA/$folder/txt \
                    $VOLUME_MOUNT_PATH/documentos_sem_justificacoes/ $VOLUME_MOUNT_PATH/log-arquivos-sem-texto.txt
        done

        mkdir -p $VOLUME_MOUNT_PATH/emendas_props_distances

    pretty_print "Calculando as distâncias entre as emendas \ne seus respectivos inteiros teores"
        EMENDAS_FOLDERPATH=$VOLUME_MOUNT_PATH/documentos_sem_justificacoes/

        #Baixa stopwords atualizadas
        python3 -c "from nltk import download;download('stopwords')"

        for folder in $(ls $EMENDAS_FOLDERPATH/); do
        echo
        echo "ID da Proposição: $folder"
            python3 coherence/inter_emd_int/inter_emd_int.py $EMENDAS_FOLDERPATH/$folder \
                coherence/languagemodel/vectors_skipgram_lei_aprovadas.bin $VOLUME_MOUNT_PATH/emendas_props_distances/
        done
fi
