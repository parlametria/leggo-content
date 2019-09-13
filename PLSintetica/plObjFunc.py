# -*- coding: utf-8 -*-

import re
import string


def PlObjCreate(path):
    # Listas de Artigos, Listas de Parágrafos, listas de incisos,
    # listas de alineas
    PlObj = []
    PlArt = []
    PlPar = []
    PlInc = []
    PlAli = []

    # Regex para encontrar níveis no texto
    artPat = re.compile(r'\nArt\. \dº. +|\nArt\. \d+. +')
    parPat = re.compile(r'\n§ \d+º|\nParágrafo único\.')
    incPat = re.compile(r'\n[MDCLXVI]+\ - +')
    aliPat = re.compile(r'\n[a-z]\)|\n[a-z][a-z]\)')
    with open(path, 'r', encoding='utf-8') as pl:
        texto = pl.read()

        arts = re.split(artPat, texto)
        for art in arts:
            if arts.index(art) == 0:
                # Acrescenta o texto anterior ao 1º artigo a lista PlObj
                PlObj.append(art)
                PlArt.append("")
                continue
            paragraphs = re.split(parPat, art)

            # Caso o próximo nível seja de parágrafo
            if len(paragraphs) > 1:
                for paragraph in paragraphs:
                    par = []
                    par.append(re.match(r'.+\b', paragraph.strip())[0])

                    incisos = re.split(incPat, paragraph)
                    if len(incisos) > 1:
                        for inciso in incisos:
                            if incisos.index(inciso) == 0:
                                PlInc.append('')
                                inc = []
                                continue

                            inc.append(re.match(r'.+\b', inciso.strip())[0])
                            alineas = re.split(aliPat, inciso)
                            if len(alineas) > 1:
                                for alinea in alineas:
                                    if alineas.index(alinea) == 0:
                                        PlAli.append("")
                                        continue
                                    PlAli.append(re.match(r'.+\b', alinea.strip())[0])

                            inc.append(PlAli)
                            PlInc.append(inc)
                            inc = []
                            PlAli = []

                    par.append(PlInc)
                    PlPar.append(par)
                    PlInc = []

                PlArt.append(PlPar)
                PlPar = []
                continue

            # Caso o próximo nível seja de inciso
            par = []
            incisos = re.split(incPat, art)
            if len(incisos) > 1:
                for inciso in incisos:
                    if incisos.index(inciso) == 0:
                        par.append(re.match(r'.+\b', inciso.strip())[0])
                        PlInc.append('')
                        inc = []
                        continue
                    inc.append(re.match(r'.+\b', inciso.strip())[0])

                    alineas = re.split(aliPat, inciso)
                    if len(alineas) > 1:
                        for alinea in alineas:
                            if alineas.index(alinea) == 0:
                                PlAli.append('')
                                continue
                            PlAli.append(re.match(r'.+\b', alinea.strip())[0])

                    inc.append(PlAli)
                    PlInc.append(inc)
                    inc = []
                    PlAli = []

                par.append(PlInc)
                PlPar.append(par)
                PlInc = []
                PlArt.append(PlPar)
                PlPar = []

            else:
                par = []
                par.append(re.match(r'.+\b', art.strip())[0])
                PlPar.append(par)
                PlArt.append(PlPar)
                par = []
                PlPar = []

        PlObj.append(PlArt)
    return (PlObj)


def num_to_ali(nr):
    letra = ''
    if float(nr/25) > 1:
        for i in range(nr//25):
            letra += string.ascii_lowercase[i]
    letra += string.ascii_lowercase[(nr % 26)]
    return letra


def ali_to_num(ali):
    if len(ali) == 1:
        valor = string.ascii_lowercase.find(ali)
        return valor + 1
    if len(ali) == 2:
        valor = 27 + string.ascii_lowercase.find(ali[1])
        return valor


def flatten(container):
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


def int_to_roman(entrada):
    """
    Converte números inteiros em números romanos. Retirado de Python Cookbook
    """
    if not isinstance(entrada, type(1)):
        raise (TypeError, "expected integer, got %s" % type(entrada))
    if not 0 < entrada < 4000:
        raise (ValueError, "Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = int(entrada / ints[i])
        result.append(nums[i] * count)
        entrada -= ints[i] * count
    return ''.join(result)


def roman_to_int(entrada):
    """
    Converte números romanos para inteiros. Retirado de Python Cookbook
    """
    if not isinstance(entrada, type("")):
        raise (TypeError, "expected string, got %s" % type(entrada))
    entrada = entrada.upper()
    nums = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    sum = 0
    for i in range(len(entrada)):
        try:
            value = nums[entrada[i]]
            # If the next place holds a larger number, this value is negative
            if i+1 < len(entrada) and nums[entrada[i+1]] > value:
                sum -= value
            else:
                sum += value
        except KeyError:
            raise (ValueError, 'entrada is not a valid Roman numeral: %s' % entrada)
    # easiest test for validity...
    if int_to_roman(sum) == entrada:
        return sum
    else:
        raise (ValueError, 'entrada is not a valid Roman numeral: %s' % entrada)


def nested_lookup(nlst, idexs):
    if len(idexs) == 1:
        return nlst[idexs[0]]
    return nested_lookup(nlst[idexs[0]], idexs[1::])


def pl_to_txt(plobj, out_name='obj_out.txt'):
    '''
    Cria um arquivo .txt do objeto pl criado
    '''
    with open(out_name, mode='w', encoding="utf8") as pl_txt:
        for i, titulo in enumerate(plobj):
            if type(titulo) == str:
                pl_txt.write(titulo)
            else:
                for j, lista_de_paragrafos in enumerate(titulo):
                    if j == 0:
                        pass
                    else:
                        for k, sublista in enumerate(lista_de_paragrafos):
                            for m, paragrafo in enumerate(sublista):
                                if type(paragrafo) == str:
                                    if k == 0:
                                        pl_txt.write('\nArt. {} {}\n'.format(j, paragrafo))
                                    else:
                                        pl_txt.write('\n§{} '.format(k) + paragrafo + '\n')
                                else:
                                    for n, lista_de_inciso in enumerate(paragrafo):
                                        if n == 0:
                                            pass
                                        else:
                                            for o, inciso in enumerate(lista_de_inciso):
                                                if type(inciso) == str:
                                                    pl_txt.write('\n{} - '.format(int_to_roman(n)) + inciso + '\n')
                                                else:
                                                    for l, lista_de_alinea in enumerate(inciso):
                                                        if l == 0:
                                                            pass
                                                        else:
                                                            pl_txt.write('\n{}) '.format(num_to_ali(l-1)) + lista_de_alinea + '\n')
