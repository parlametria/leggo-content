Contém todos arquivos necessários para treinar um modelo de segmentação e utilizá-lo para segmentar arquivos de emendas diversos.
A pasta já contém um modelo pré-treinado (modelo.model) e seus resultados (resultados_janela_4.txt).

Metodologia:
	1. Rodar o treino pelo comando "treino_segmentador.py local1 arq1 local2" para treinar o modelo, sendo:
		local1 -> local com os arquivos de treino
		arq1 -> nome do arquivo que conterá o binário do modelo
		local2 -> local para salvar os resultados obtidos

	2. Rodar o segmentador através do comando "segmentador_generico.py local1 arq1 local2" para segmentar os textos das emendas e salvar o que foi predito em arquivos (um arquivo por emenda), sendo:
		local1 -> local com os arquivos que se deseja segmentar
		arq1 -> nome do arquivo que contém o binário do modelo já treinado (arq1 do passo anterior)
		local2 -> local para salvar as predições (segmentos obtidos)
		
	3. Rodar o organizador de segmentos em blocos pelo comando "divide_predicao_em_blocos.py local1 local2" para separar a predição em blocos (apenas pra organização), sendo:
		local1 -> local com os arquivos preditos (local2 do passo anterior)
		local2 -> local para salvar os arquivos divididos em blocos


