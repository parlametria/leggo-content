import requests
import time
import sys
from bs4 import BeautifulSoup
import httplib2

def meta_redirect(content):
	soup  = BeautifulSoup(content)

	result = soup.find("meta",attrs={"http-equiv":"refresh"})
	if result:
		wait,text=result["content"].split(";")
	if text.strip().lower().startswith("url="):
		url = text[4:]
		return url
	return None


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

headers = {'user_agent': user_agent}

def operacoes_obtencao_arquivos_csv():
	'''
		Operações de coleta de arquivos, para cada linha do .csv tenta coletar o teor da emenda (muitas emendas não têm pdfs e, portanto,
		não são coletadas).
	'''

	with open('emendas_tab.tsv', 'r') as arquivo:
		linhas = arquivo.readlines()


	with open('linha_atual_csv.txt', 'r') as arquivo:
		indices = arquivo.readlines()
		linha_no_csv = int(indices[0])
		linha_inicio = int(indices[1])
		linha_final = int(indices[2])

	for linha in linhas[linha_inicio:linha_final]: #para cada emenda
		try:
			campos = linha.split('\t') #separa em campos

			nome_arquivo = campos[2] #para salvar o teor da emenda
			link_emenda = campos[9] #para baixar a emenda
	
			print(nome_arquivo)
			print(link_emenda)

			time.sleep(2)
			resp = requests.get(link_emenda, allow_redirects = True)

                	# follow the chain of redirects
			while meta_redirect(resp.content):
				resp = requests.get(meta_redirect(resp.content), allow_redirects = True) 
			print(resp.url)

			if resp.status_code == 200: #se houve sucesso e se trata-se de um pdf
				with open('teores_emendas/' + nome_arquivo.replace('/', '___').replace(' ', '_') + '.html', 'wb') as arquivo: #salva substituindo caracteres especiais por válidos 
					arquivo.write(resp.content)

				with open('log_sucessos.txt', 'a') as arquivo: #salva o nome
					arquivo.write('\n' + str(linha_no_csv) + '\n' + nome_arquivo.replace('/', '___').replace(' ', '_') + '\n' + str(resp.status_code) + '\n' + resp.headers['content-type'] + '\n')

			else: #se houve erro
				with open('log_erros.txt', 'a') as arquivo: #salva o nome
					arquivo.write('\n' + str(linha_no_csv) + '\n' + nome_arquivo.replace('/', '___').replace(' ', '_') + '\n' + str(resp.status_code) + '\n' + resp.headers['content-type'] + '\n')

			linha_no_csv += 1
			with open('linha_atual_csv.txt', 'w') as arquivo:
				arquivo.write(str(linha_no_csv) + '\n')
				arquivo.write(str(linha_no_csv) + '\n') #a linha de início passa a ser a atual
				arquivo.write(str(linha_final) + '\n') #a final se mantém
			#sys.exit(-1)
		
		except:
			linha_no_csv += 1
			with open('linha_atual_csv.txt', 'w') as arquivo: #se houve erro na linha, ignora e passa para a próxima
                                arquivo.write(str(linha_no_csv) + '\n')
                                arquivo.write(str(linha_no_csv) + '\n') #a linha de início passa a ser a atual
                                arquivo.write(str(linha_final) + '\n') #a final se mantém

def main():
	operacoes_obtencao_arquivos_csv()



if __name__ == "__main__":
    main()




