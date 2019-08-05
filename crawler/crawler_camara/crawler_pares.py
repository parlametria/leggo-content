# Crawler desenvolvido para obter os textos iniciais (PLs ou MPVs) e textos finais (publicados no Diário da União) do site da Câmara
#
# Algoritmo:
#	Para cada ano do arquivo de paginação
#		Clica no link que leva aos links de PLs/MPVs desse ano
#			Acessa o link do texto publicado
#			Salva em um .txt o texto publicado
#			Acessa o link do PL/MPV inicial
#			Salva o .pdf do PL/MPV inicial



from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
from requests.exceptions import *
import re
import time
import sys



###################################################
################################################### Funções
###################################################
def inicia_acesso(url): #inicia webdriver
	driver = webdriver.Firefox()
	driver.implicitly_wait(30)
	driver.get(url)
	driver.find_element_by_id("ide").click() #para expandir os anos visíveis

	return driver



def encontra_elemento_ano(soup_principal, anos, indice_anos):
	lista_li = soup_principal.find("li", {"id": "id2"})
	lista_anos_site = lista_li.find_all('li')
	for elem in lista_anos_site:
		if(anos[indice_anos] in elem.text): #se for o ano atualmente procurado
			print(elem.a['href'])
			break

	return elem



def obtem_links_dos_textos(link_para_PL_MPV, anos, indice_anos):
	inicio_link = link_para_PL_MPV.split('lei-')[0] #salva parte inicial para o próximo passo, no qual só uma parte da url é fornecida no html

	############################ Página PL ou MPV
	fonte_PL_MPV = requests.get(link_para_PL_MPV)
	fonte_PL_MPV = fonte_PL_MPV.text
	aux_diaemes = link_para_PL_MPV.split('lei-')[1].split('-')
	dia_e_mes = aux_diaemes[1] + '_' + aux_diaemes[2] + '_'
	soup_PL_MPV = BeautifulSoup(fonte_PL_MPV, 'lxml')

	divdadosNorma = soup_PL_MPV.find('div', class_ = 'dadosNorma')

	classe_sessao = divdadosNorma.find_all('div', class_ = 'sessao')
	valido = 0
	for cont_sess in range(0, len(classe_sessao)):
		if("Proposição Originária:" in classe_sessao[cont_sess].text):
			valido = 1
			break
	if(valido == 0): #se não há proposição originária
		with open("log.txt", "a") as arquivo:
			arquivo.write(anos[indice_anos] + "_" + "^^^" + "SPO^^^" + "Sem Proposição Originária^^^" + link_para_PL_MPV + "\n")
		pass

	link_publicado = inicio_link + classe_sessao[0].a['href'] #primeira div com class sessao dentro da div com class dadosNorma
	link_originaria = classe_sessao[cont_sess].a['href'] #segunda div com class sessao dentro da div com class dadosNorma
	numero_PL_MPV = "_" + classe_sessao[cont_sess].a.string.replace(" ", "_").replace("/", "__") + "_"

	return link_publicado, link_originaria, numero_PL_MPV, dia_e_mes



def obtem_texto_publicado(link_publicado, anos, indice_anos, numero_PL_MPV, link_para_PL_MPV):
	time.sleep(0.1)
	fonte_publicado = requests.get(link_publicado)
	fonte_publicado = fonte_publicado.text
	#print(fonte_publicado)
	soup_publicado = BeautifulSoup(fonte_publicado, 'lxml')
	texto_publicado = soup_publicado.find('div', class_ = 'texto')
	if(texto_publicado is None):
		with open("log.txt", "a") as arquivo:
			arquivo.write(anos[indice_anos] + "_" + str(numero_PL_MPV) + "^^^" + "STP^^^" + "Sem Texto Publicado^^^" + link_para_PL_MPV + "\n")
		raise Exception

	texto_publicado = texto_publicado.text

	return texto_publicado



def obtem_texto_original_e_html_tramitacao(link_originaria, anos, numero_PL_MPV, link_para_PL_MPV, indice_anos):
	time.sleep(0.1)
	aux = requests.get(link_originaria, allow_redirects = True)
	aux = aux.url

	fonte_originaria = requests.get(aux, allow_redirects = True)
	fonte_originaria = fonte_originaria.text

	soup_originaria = BeautifulSoup(fonte_originaria, 'lxml')

	aux = soup_originaria.find('a', class_ = 'rightIconified iconDetalhe linkDownloadTeor')['href']
	if(aux is None or 'Tramitacao' in aux):
		with open("log.txt", "a") as arquivo:
			arquivo.write(anos[indice_anos] + "_" + str(numero_PL_MPV) + "^^^" + "TAT^^^" + "Texto Apenas na Tramitação^^^" + link_para_PL_MPV + "\n")
		raise Exception #ou seja, o link existe mas é só em fase de tramitação: não há um texto de PL original
	aux = aux.split('?')[1]

	link_download = 'http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?' + aux

	requisicao = requests.get(link_download, allow_redirects = True)
	if("page=" in requisicao.url or "PAGE=" in requisicao.url): #se na url final após os redirecionamentos há uma indicação de página então está num diário maior
		with open("log.txt", "a") as arquivo:
			arquivo.write(anos[indice_anos] + "_" + str(numero_PL_MPV) + "^^^" + "TD^^^" + "Texto em Diário^^^" + link_para_PL_MPV + "\n")
		raise Exception


	if("Licensed to the Apache Software Foundation (ASF)" in str(requisicao.content)): #só possui essa string se o link para o pdf NÃO existe
																						#e nesse caso o binário (.pdf) contém exatamente essa string e podemos fazer str(requisicao.content)
		with open("log.txt", "a") as arquivo:
			arquivo.write(anos[indice_anos] + "_" + str(numero_PL_MPV) + "^^^" + "SP^^^" + "Sem PDF^^^" + link_para_PL_MPV + "\n")
		raise Exception #e então levanta uma exceção
	else:
		print('com pdf')

	return requisicao, fonte_originaria



def obtem_link_proxima_pagina(driver):
	lista_ul_li = driver.find_element_by_class_name("proxima") #encontra o elemento com o link para a próxima página (elemento único)

	try: #tenta obter link da próxima página
		link = lista_ul_li.find_element_by_tag_name("a") #obtem o link desse elemento
		return link
	except NoSuchElementException: #se não tiver link, acabou a paginação desse ano
		return "sai_loop"



def salva_dados(anos, dia_e_mes, numero_PL_MPV, fonte_originaria, texto_publicado, requisicao, link_para_PL_MPV, link_originaria, link_publicado, indice_anos):
	with open(sys.argv[1] + '/doc_' + anos[indice_anos] + "_" + dia_e_mes + str(numero_PL_MPV) + '.txt', 'w') as arquivo:
		arquivo.write(fonte_originaria)

	with open(sys.argv[2] + '/doc_' + anos[indice_anos] + "_" + dia_e_mes  + str(numero_PL_MPV) + '.txt', 'w') as arquivo:
		arquivo.write(texto_publicado)

	with open(sys.argv[3] + '/doc_' + anos[indice_anos] + "_" + dia_e_mes + str(numero_PL_MPV) + '.pdf', 'wb') as arquivo:
		arquivo.write(requisicao.content)

	with open('relatorio.txt', 'a') as arquivo:
		arquivo.write('doc_' + anos[indice_anos] + "_" + dia_e_mes + str(numero_PL_MPV) + '\n')
		arquivo.write(link_para_PL_MPV + '\n')
		arquivo.write(link_originaria + '\n')
		arquivo.write(link_publicado + '\n')
		arquivo.write('\n')



def atualiza_arquivo_anos(anos, indice_anos):
	with open("paginacao_por_anos.txt", "w") as arquivo: #atualiza o arquivo de anos deixando apenas os que faltam. se ocorrer exceção maior ou erro o programa reinicia e continua de onde parou
		for aux_anos in range(indice_anos, len(anos)):
			arquivo.write(str(anos[aux_anos]) + '\n')



###################################################
################################################### Programa principal
###################################################
def main():
	url = "http://www2.camara.leg.br/busca/?o=relevance&v=legislacao&colecao=S&conteudolegin=&numero=&ano=&tiponormaF=Lei+Ordin%C3%A1ria" #página inicial, fixa

	with open("paginacao_por_anos.txt", "r") as arquivo:
		anos = arquivo.readlines()

	for i in range(0, len(anos)):
		anos[i] = anos[i].replace('\n', '') #deixa apenas o valor do ano

	contador_documentos = 1 #para visualização no terminal
	indice_anos = 0 #alterar conforme necessário

	for cont in anos: #cont não é utilizado, apenas para o loop
		driver = inicia_acesso(url)
		#print(driver.page_source)

		soup_principal = BeautifulSoup(driver.page_source, 'lxml') #inicia coletando a página inicial

		elem = encontra_elemento_ano(soup_principal, anos, indice_anos)

		driver.find_element_by_css_selector("a[href='" + elem.a['href'] + "']").click() #vai para a página referente ao ano em questão
		soup_principal = BeautifulSoup(driver.page_source, 'lxml') #atualiza o objeto beautifulsoup para a página clicada
	
		while(1): #acaba quando não houverem mais páginas
			for link_para_PL_MPV in soup_principal.find_all('span', class_ = 'titulo'): #todos spans com classe titulo em cada página inicial contém um link
				time.sleep(0.2)
				try: #para o caso de alguma das tags e classes mencionadas no código não existir na coleta em questão ou afins
					link_para_PL_MPV = link_para_PL_MPV.a['href']

					link_publicado, link_originaria, numero_PL_MPV, dia_e_mes = obtem_links_dos_textos(link_para_PL_MPV, anos, indice_anos)

					############################ Página do texto publicado
					texto_publicado = obtem_texto_publicado(link_publicado, anos, indice_anos, numero_PL_MPV, link_para_PL_MPV)

					############################ Página do texto original
					requisicao, fonte_originaria = obtem_texto_original_e_html_tramitacao(link_originaria, anos, numero_PL_MPV, link_para_PL_MPV, indice_anos)
				
					############################ Salvando os arquivos (colocados no final para que o bloco try-except funcione corretamente)
					salva_dados(anos, dia_e_mes, numero_PL_MPV, fonte_originaria, texto_publicado, requisicao, link_para_PL_MPV, link_originaria, link_publicado, indice_anos)

					print(contador_documentos)
					contador_documentos += 1

				except Exception as e:
					print(e)
					pass #se houver alguma exceção simplesmente segue tentando com os outros links


			link = obtem_link_proxima_pagina(driver)
			if(link == "sai_loop"): #se não retornar um link a paginação deste ano acabou, então sai do loop
				break
			link.click() #clica no link, e agora o objeto driver está na próxima página pra onde o link leva

			soup_principal = BeautifulSoup(driver.page_source, 'lxml') #atualiza o objeto soup principal
			#driver.implicitly_wait(30)

		indice_anos += 1 #atualiza o ano que será coletado

		atualiza_arquivo_anos(anos, indice_anos)

		driver.quit() #fecha o driver e a sessão
		time.sleep(2) #espera um tempo e retorna, abrindo o webdriver novamente (início do loop)


if __name__== "__main__":
	main()
