import pandas as pd
import os
import sys
import urllib.request
import unidecode

emendas_links = sys.argv[1]
output_dir = sys.argv[2]
inteiro_links = sys.argv[3]

def download_pdfs_from_path(csv_path):
  df = pd.read_csv(csv_path)
  
  count_tipo = {}
  
  for idx, row in df.iterrows():
  
      link = row["link_inteiro_teor"]
      id_proposicao = str(row["id_proposicao"])
      cd_texto = str(row["codigo_texto"])
  
      full_outputpath = os.path.join(output_dir, id_proposicao)
  
      if not(os.path.exists(full_outputpath)):
          os.mkdir(full_outputpath)
  
      full_outputpath = os.path.join(full_outputpath, "pdf")
      if not(os.path.exists(full_outputpath)):
          os.mkdir(full_outputpath)
  
      tipo = unidecode.unidecode(row["tipo_texto"].lower())
  
      file_name_tipo = "%s_%s_%s.pdf" % (cd_texto, id_proposicao, tipo.replace(" ","_"))
      file_name = os.path.join(full_outputpath, file_name_tipo)
      print(file_name)
      urllib.request.urlretrieve(link, file_name)


download_pdfs_from_path(emendas_links)
download_pdfs_from_path(inteiro_links)
