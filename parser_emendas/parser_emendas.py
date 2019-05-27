class Emenda:
	def __init__(self, local):
		with open(local, 'r') as arquivo:
			texto = arquivo.read()

		self.Artigos, self.Paragrafos, self.Alineas  = self.parserEmenda(texto)


	def parserEmenda(texto):
		lista_artigos = []
		lista_paragrafos = []
		lista_alineas = []

		'''
		código do parser
		'''
		
		return lista_artigos, lista_paragrafos, lista_alineas
		

'''		
	emenda1 = Emenda('emenda1.txt')

	estrutura1
		substrutura1
			substrutura2

	f1(arigo not null, par, al):
		


	listA = []
	listaP = []
	listaAL = []

	
		
emenda1[1][2][3]
#emenda1['Art1']['Par2']['Alinea3']
'''
