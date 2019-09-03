'''
Organiza as predições dividindo cada predição em blocos
'''

import os
import sys

def le_arquivo(arq):
	with open(sys.argv[1] + '/' + arq, 'r') as atual:
		texto = atual.readlines()

	return texto


def salva_arquivos(arq, cont_bloco, bloco_atual):
	with open(sys.argv[2] + '/' + arq + '/bloco_' + str(cont_bloco), 'w') as arq_bloco:
		for token in bloco_atual:
			arq_bloco.write(token)


def divide_em_blocos():
	arquivos = os.listdir(sys.argv[1] + '/')

	for arq in arquivos:
		print(arq)
		os.mkdir(sys.argv[2] + '/' + arq)
		texto = le_arquivo(arq)


		cont_bloco = 1
		bloco_atual = []
		i = 0
		while i < len(texto):
			print(i)
			try:
				tag = texto[i].split()[1]
			except: #alguns raros casos possuem uma linha em branco contendo apenas a tag, devemos apenas ignorar estas linhas
				i += 1
				pass
			if tag == 'O':
				bloco_atual.append(texto[i])
			else: #se for I
				salva_arquivos(arq, cont_bloco, bloco_atual)
				bloco_atual = []
				bloco_atual.append(texto[i])					
				cont_bloco += 1
			i += 1

		salva_arquivos(arq, cont_bloco, bloco_atual)


def main():
	divide_em_blocos()


if __name__ == "__main__":
	main()


