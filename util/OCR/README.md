Instalar dependências

	sudo apt-get install tesseract-ocr
	pip install pytesseract
	pip install pillow
	sudo apt-get install imagemagick
	pip install wand

	sudo apt-get install tesseract-ocr-por
		para instalar em português, via https://askubuntu.com/questions/793634/how-do-i-install-a-new-language-pack-for-tesseract-on-16-04


Arrumar bugs:
No arquivo /etc/ImageMagick-6/policy.xml (ou /etc/ImageMagick/policy.xml):

	*comentar a linha
    <!-- <policy domain="coder" rights="none" pattern="MVG" /> -->


    	*alterar a linha
    <policy domain="coder" rights="none" pattern="PDF" />

    para

    <policy domain="coder" rights="read|write" pattern="PDF" />


    	*adicionar a linha
    <policy domain="coder" rights="read|write" pattern="LABEL" />

		via https://stackoverflow.com/questions/42928765/convertnot-authorized-aaaa-error-constitute-c-readimage-453


Além disso é importante ressaltar que o programa irá guardar as figuras em um cache definido no policy.xml, portanto alguns problemas com relação a espaço podem acabar surgindo. Observar o que está descrito na seguinte página do stack overflow: https://stackoverflow.com/questions/51554980/oserror-errno-12-cannot-allocate-memory-pytesseract



Tutoriais:
	https://github.com/nikhilkumarsingh/tesseract-python
	https://www.youtube.com/watch?v=jWh0FaRRZC4
	https://www.youtube.com/watch?v=RGSoVGtuHuA




Após as configurações, para executar o programa basta rodar o comando "python3 conversor_OCR local1 local2", sendo local1 o diretório com os PDFs a serem convertidos e local2 o diretório destino dos textos obtidos da conversão.
