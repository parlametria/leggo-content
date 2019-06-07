#!/bin/bash


#Gera a tabela com os links para os arquivos dos textos e emendas
Rscript ../versoes-de-proposicoes/fetcher.R -i ../leggoR/data/tabela_geral_ids_casa.csv -e ../leggo-backend/data/emendas_raw.csv -o novas_emendas.csv -a avulsos_iniciais.csv

#Verifica se há novas emendas
if [ $(cat novas_emendas.csv | wc -l) -lt 2 ]
then
    echo "Não há novas emendas"
    exit 0
else
    mkdir -p emendas

    #Entra na pasta data do leggo-content
    cd util/data/

    #Download dos arquivos em pdf
    python3 download_csv_prop.py ../../../versoes-de-proposicoes/novas_emendas.csv ../../../versoes-de-proposicoes/emendas/ 
    python3 download_csv_prop.py ../../../versoes-de-proposicoes/avulsos_iniciais.csv ../../../versoes-de-proposicoes/emendas/ 

    #Converte de pdf para txt
    ./calibre_convert.sh ../../../versoes-de-proposicoes/emendas

    #Verifica se os pdfs baixados eram imagens
    python verifica_se_pdf_imagem.py ../../../versoes-de-proposicoes/emendas

    #Separa Justificacoes
    #Pasta com as emendas
    DIR_DATA="../../../versoes-de-proposicoes/emendas"

    for folder in $(ls $DIR_DATA/); do
            echo $DIR_DATA/$folder/txt
            python3 ../tools/SepararJustificacoes.py $DIR_DATA/$folder/txt ./emendas_sem_justificacoes/
    done

    mkdir -p emendas_all_dist

    #Calcula todas as distancias para todas as props
    ../../coherence/inter_emd_int/chama_inter_emd_int_para_todas_props.sh emendas_sem_justificacoes/

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







