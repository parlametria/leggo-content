import pandas as pd
import os
import sys
import urllib.request
import unidecode
import traceback

def print_usage():
  print("Número errado de parâmetros,o certo é: donwload_csv_props.py <caminho_csv_links_arquivos> <campo_prop_id> <campo_doc_id> <tipo_texto> <output_dir>")

def download_pdfs_from_path(csv_path, campo_prop_id, campo_doc_id, tipo_texto, output_dir):
  df = pd.read_csv(csv_path)
  
  count_tipo = {}
  
  for idx, row in df.iterrows():

      try:
  
        link = row["inteiro_teor"]
        casa = row["casa"]
        id_proposicao = str(row[campo_prop_id])
        cd_texto = str(row[campo_doc_id])

        full_outputpath = os.path.join(output_dir, id_proposicao, "pdf")
        os.makedirs(full_outputpath, exist_ok=True)
  
        file_name_tipo = "%s_%s_%s_%s.pdf" % (cd_texto, id_proposicao, casa, tipo_texto)
        file_name = os.path.join(full_outputpath, file_name_tipo)
        print(str(link),'->',file_name)
        urllib.request.urlretrieve(link, file_name)
      except:
          print(traceback.format_exc())

if (len(sys.argv) != 6):
  print_usage()
else:
  links_arquivos = sys.argv[1]
  campo_prop_id = sys.argv[2]
  campo_doc_id = sys.argv[3]
  tipo_texto = sys.argv[4]
  output_dir = sys.argv[5]

  download_pdfs_from_path(links_arquivos, campo_prop_id, campo_doc_id, tipo_texto, output_dir)
