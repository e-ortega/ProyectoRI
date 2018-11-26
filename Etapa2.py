#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import math
import requests
from os import walk
from http import HTTPStatus
from bs4 import BeautifulSoup
from bs4.element import Comment

# este es el vector de palabras que se llena con palabras que se deben omitir en los textos
plain_text_dir = "plain_text"
posting_file = ""
path = os.path.dirname(os.path.realpath(__file__))
global_words_list = []
stop_words = []
total_frequency_list = []
document_quantity_list = []
requests_errors = []
tok_path = ""


def run():
    # create your subdirectory
    if not os.path.exists(os.path.join(path, plain_text_dir)):
        os.mkdir(os.path.join(path, plain_text_dir))

    fill_stop_words()
    procesaConsulta("Que hace barato auto")
    #read_urls()
    #generate_error_page_file()
    #print("Calculando pesos")
    #calculePeso()
    #indice(r"\posting.txt")
    print("Termina")


# llena el vector stop_words usando la  lista de palabras que se deben omitir
def fill_stop_words():
    file_name = "stopwords.txt"
    file = open(file_name, 'r', encoding="utf-8")
    for line in file:
        for word in line.split():  # para que no salga el \n
            stop_words.append(word)


# lee de un archivo y debe substraer el url al que se quiere ingresar y el nombre del archivo
def read_urls():
    file_name = "urles.txt"
    file = open(file_name, "r", encoding="utf-8")
    for line in file:
        separator = []
        for word in line.split():
            separator.append(word)
        html_parser(separator)


# substrae el texto de un html y lo guarda en un archivo
def html_parser(separator):
    name = str(separator[0])
    name = name.replace(u'\ufeff', '')
    file_name = name + '.txt'
    file_name = file_name.replace(".html", "")
    file_dir = os.path.dirname(__file__)

    abs_file_path = file_dir + "/Coleccion" + '/' + name
    page = open(abs_file_path, 'r', encoding="utf-8")
    print("Parseando :" + name)
    soup = BeautifulSoup(page, 'html.parser')
    text = soup.findAll(text=True)
    visible_texts = filter(tag_visible, text)
    texts = u" ".join(t.strip() for t in visible_texts)
    path_file = os.path.join(path, plain_text_dir, file_name)

    # create an empty file.
    try:
        file_text = open(path_file, '+w', encoding="utf-8")
        file_text.write(texts)
        file_text.close()
        tokenizer(path_file)
    except IOError:
        print("Algo pasó creando el archivo el documento: [%s].", file_name)



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


# lee el archivo sin bloques html dado por htmlParser, recorre cada palabra, la busca en stop_words, si no la encuentra
# la busca en el vector de palabras, si la encuentra le suma 1 en la posicion de caso contrario la agrega con un 1
def tokenizer(file_name):
    word_list = []
    frequency_list = []
    file = open(file_name, "r", encoding="utf-8")

    for line in file:
        for word in line.split():
            try:

                valid_word = True
                word = word.lower()
                word = re.sub(r'\W+', '', word)  # se eliminan caracteres no alfanumericos
                if not word.isalnum():
                    valid_word = False
                if len(word) < 2 or len(word) > 30:
                    valid_word = False  # no se usan palabras de tamaño mayor a 30
                if len(word) > 0:
                    if not word.isdigit() and not word[0].isalpha():
                        valid_word = False  # no se usan palabras que no sean solo numeros y no empiecen por a-z ej: 3arbol

                if not stop_words.__contains__(word) and valid_word:
                    if word_list.__contains__(word):
                        frequency_list[word_list.index(word)] += 1
                    else:
                        word_list.append(word)
                        frequency_list.append(1)

                    if global_words_list.__contains__(word):
                        total_frequency_list[global_words_list.index(word)] += 1
                    else:
                        document_quantity_list.append(0)
                        global_words_list.append(word)
                        total_frequency_list.append(1)

            except Exception as error:
                print("[" + str(word) + "]" + error.__str__())
                requests_errors.append(file_name)
    for word in word_list:
        document_quantity_list[global_words_list.index(word)] += 1
    normalize_frequency(file_name, word_list, frequency_list)


# crea vectores con las frecuencias relativas de los terminos de un documneto
def normalize_frequency(file_name, word_list, frequency_list):
    if len(frequency_list) > 0 and len(word_list) > 0:
        normalized_frequency_list = []
        max_frequency = max(frequency_list)
        for frequency in frequency_list:
            normalized_value = frequency / max_frequency
            normalized_frequency_list.append(normalized_value)
        create_tok(file_name, word_list, normalized_frequency_list, frequency_list)
        create_vocabulary()
    else:
        requests_errors.append(file_name)


# crea un archivo .tok a partir de los vectores de palabras y frecuencias normalizadas
def create_tok(file_name, word_list, normalized_frequency_list, frequency_list):
    # global tok_path
    tok_path = r'.\plain_text\tok'
    if not os.path.exists(tok_path):
        os.makedirs(tok_path)
    file_name = file_name + '.tok'
    file_name = file_name.replace(".txt", "")
    index = file_name.find('plain_text')
    file = file_name[:index + len('plain_text')] + r'\tok' + file_name[index + len('plain_text'):]
    for passnum in range(1, len(word_list)):
        i = 0
        for element in range(0, len(word_list) - passnum):
            if word_list[i] > word_list[i + 1]:
                temp = word_list[i]
                word_list[i] = word_list[i + 1]
                word_list[i + 1] = temp
                temp = normalized_frequency_list[i]
                normalized_frequency_list[i] = normalized_frequency_list[i + 1]
                normalized_frequency_list[i + 1] = temp
                temp = frequency_list[i]
                frequency_list[i] = frequency_list[i + 1]
                frequency_list[i + 1] = temp
            i += 1

    try:
        file_text = open(file, '+w', encoding="utf-8")
        vector_str = [str(i) for i in normalized_frequency_list]
        vector_frequency = [str(i) for i in frequency_list]
        counter = 0
        for word in word_list:
            # file_text.write(word + "," + vector_str[counter] + "," + vector_frequency[counter] + "\n")
            file_text.write(word + " " * (30 - len(word)) + ", " + vector_str[counter]+ " " + " " * (
                        12 - len(vector_str[counter])) + " , " + vector_frequency[counter] + " " * (
                                        20 - len(vector_frequency[counter])) + "\n")
            counter += 1
        file_text.close()
    except IOError:
        print("Algo pasó creando el .tok para el documento: [%s].", file_name)


#Hace un sort para 3 lista, tomando como ordenamiento la lista base, este algorito es utilizado para ordenar el vocabulario
def merge_sort_3_listas(lista_base, lista1, lista2):
    if len(lista_base)>1:
        medio = len(lista_base)//2
        mitad_iz_base = lista_base[:medio]
        mitad_de_base = lista_base[medio:]

        mitad_iz1 = lista1[:medio]
        mitad_de1 = lista1[medio:]

        mitad_iz2 = lista2[:medio]
        mitad_de2 = lista2[medio:]

        merge_sort_3_listas(mitad_iz_base, mitad_iz1, mitad_iz2)
        merge_sort_3_listas(mitad_de_base, mitad_de1, mitad_de2)

        i=0
        j=0
        k=0

        while i < len(mitad_iz_base) and j < len(mitad_de_base):
            if mitad_iz_base[i] < mitad_de_base[j]:
                lista_base[k] = mitad_iz_base[i]
                lista1[k] = mitad_iz1[i]
                lista2[k] = mitad_iz2[i]
                i=i+1
            else:
                lista_base[k] = mitad_de_base[j]
                lista1[k] = mitad_de1[j]
                lista2[k] = mitad_de2[j]
                j=j+1
            k=k+1

        while i < len(mitad_iz_base):
            lista_base[k] = mitad_iz_base[i]
            lista1[k] = mitad_iz1[i]
            lista2[k] = mitad_iz2[i]
            i=i+1
            k=k+1

        while j < len(mitad_de_base):
            lista_base[k] = mitad_de_base[j]
            lista1[k] = mitad_de1[j]
            lista2[k] = mitad_de2[j]
            j=j+1
            k=k+1


# crea el archivo vabulario
def create_vocabulary():
    file_name = 'Vocabulario.txt'
    file_name = os.path.join(path, plain_text_dir, file_name)

    merge_sort_3_listas(global_words_list, total_frequency_list, document_quantity_list)
    
    try:
        file_text = open(file_name, '+w', encoding="utf-8")
        vector_frequency = [str(i) for i in total_frequency_list]
        vector_quantity = [str(i) for i in document_quantity_list]
        counter = 0
        for word in global_words_list:
            file_text.write(str(word) + " " + ", " + str(vector_frequency[counter])+ " " + ", " + str(vector_quantity[counter]) + "\n")
            counter += 1
        file_text.close()
    except IOError:
        print("Algo pasó creando el .tok para el documento: [%s].", file_name)


def generate_error_page_file():
    file_name = 'errores.txt'
    file_name = os.path.join(path, plain_text_dir, file_name)
    try:
        file_text = open(file_name, '+w', encoding="utf-8")
        for word in requests_errors:
            file_text.write(str(word) + "\n")

        file_text.close()
    except IOError:
        print("Algo pasó creando el .tok para el documento: [%s].", file_name)


#Crea in Indice a partir del archivo posting
def indice(archivo):
    archivo = archivo.replace(".\\", "\\")
    file_name = 'Indice.txt'
    file_name = os.path.join(path, plain_text_dir, file_name)
    # resultado = os.path.join(path, plain_text_dir, archivo)
    resultado = file_name.replace("\\plain_text\\Indice.txt", archivo)
    print(resultado)
    try:
        lines = []
        with open(resultado, encoding="utf8") as file:
            for line in file:
                line = line.strip()
                lines.append(line)
    except Exception as e:
        print(e)
    c = 0
    for l in lines:
        pos = l.find(" ")
        #pos = l.find(",")
        lines[c] = l[:pos]
        c = c+1
    termino=" "
    c=0
    try:
        file_text = open(file_name, '+w', encoding="utf-8")
        numeroVeces = 0
        for l in lines:
          numeroVeces += 1
          if (termino != l):
                termino = l
                file_text.write(termino + " " * (30-len(termino)) + ", " + str(c) + " " * (12-len(str(c))) + ", " + str(numeroVeces)+"\n")
                numeroVeces = 0
          c = c+1
    except IOError:
        print("Algo pasó creando el archivo Indice")


def calculaPesos(frecuenciaNormalizada, frecuenciaInversa):
    return frecuenciaNormalizada * frecuenciaInversa


def loadVocabulario(palabras, frecuencias):
    #file_name = 'vocabulario.txt'
    cur_path = os.path.dirname(__file__)
    a = cur_path + '/plain_text/Vocabulario.txt'
    #a = 'C:/Users/Jose M/Google Drive/II Semestre 2018/Proyecto/plain_text/Vocabulario.txt'
    with open(a, 'r', encoding="utf-8") as file:
        for line in file:
            count = 0
            for word in line.split():
                if count == 0:
                    palabras.append(word)
                    count = count + 1
                elif count == 2:
                    frecuencias.append(word)
                    count = count + 1
                else:
                    count = count +1


def calculePeso():
    palabras = []
    frecuencias = []
    palabrasTok = []
    frecuenciasTok = []
    palabraPeso = []
    pesos=[]
    loadVocabulario(palabras,frecuencias)
    cur_path = os.path.dirname(__file__)
    tok_path = cur_path + "/plain_text/tok"
    dir_path_name = r'.\plain_text\wtd'
    dir_path_posting = r'.\plain_text\posting.txt'
    file_posting = open(dir_path_posting, '+w', encoding="utf-8")
    if not os.path.exists(dir_path_name):
        os.makedirs(dir_path_name)
    f = []
    for (dirpath, dirnames, filenames) in walk(tok_path):
        f.extend(filenames)
        break
    for n in range (0, len(f)):

        file_name = tok_path + "/"+f[n]
        print("creando tok %s", file_name)
        file = open(file_name, 'r', encoding="utf-8")
        for line in file:
            wordCount = 0
            for word in line.split():
                if wordCount == 0:
                    palabrasTok.append(word)
                    wordCount = wordCount + 1
                elif wordCount == 2:
                    frecuenciasTok.append(word)
                    wordCount = wordCount +1
                else:
                    wordCount = wordCount + 1
        for i in range (0, len(palabrasTok)):
            for j in range (0, len(palabras)):
                if palabras[j] == palabrasTok[i]:
                    palabraPeso.append(palabrasTok[i])
                    pesos.append(float(frecuenciasTok[i]) * float(frecuencias[j]))
        file_name = cur_path+ "/plain_text/wtd/"+f[n] + ".wtd"
        file_name = file_name.replace(".tok", "")
        file_text = open(file_name, '+w', encoding="utf-8")
        for k in range (0, len(palabraPeso)):
            file_text.writelines(str(palabraPeso[k])+ "   "+str(pesos[k]) + "\n")
            file_posting.writelines(str(palabraPeso[k])+"   "+f[n].replace(".txt.tok","")+ "   "+str(pesos[k]) + "\n")
        file_text.close()
        palabrasTok = []
        frecuenciasTok = []
        palabraPeso = []
        pesos = []
    file_posting.close()
    global posting_file
    posting_file = dir_path_posting
    inputFile = open(dir_path_posting, 'r', encoding="utf-8")
    lineList = inputFile.readlines()
    inputFile.close()
    lineList.sort()
    with open(dir_path_posting, 'w', encoding="utf-8") as f:
        for line in lineList:
            f.write(line)




def procesaConsulta(consulta):
    vecConsulta = []
    consultaCont = []
    words = consulta.split()

    #en esta parte solo saca palabras y calcula  la frecuencia(freqij)
    for word in words:
        word = word.lower()
        if stop_words.__contains__(word):
            print("something")
        else:
            if vecConsulta.__contains__(word) == False:
                vecConsulta.append(word)
                consultaCont.append(1)
            else:
                index = vecConsulta.index(word)
                consultaCont[index] = consultaCont[index] + 1

    #calcula freq normalizada(tfij)

    maximoIndex = max(consultaCont)
    freqNormQ = []

    for i in range(0, len(consultaCont)):
        freqNormQ .append(consultaCont[i]/maximoIndex)


    #Cargue Vocabulario
    cur_path = os.path.dirname(__file__)
    vocPalabras = []
    vocNumTer = []
    vocFrqInv = []

    file_name = cur_path + "/plain_text/Vocabulario.txt"
    file = open(file_name, 'r', encoding="utf-8")

    for line in file:
        count = 0
        for entry in line.split():
            if count == 0:
                vocPalabras.append(entry)
                count = count + 1
            elif count == 2:
                vocNumTer.append(entry)
                count = count + 1
            elif count == 4:
                vocFrqInv.append(entry)
                count = count + 1
            else:
                count = count + 1


    #calcule pesos(wij)
    wijQ = []

    for i in range(0, len(freqNormQ)):
        word = vecConsulta[i]

        if vocPalabras.__contains__(word):
            vocIndex = vocPalabras.index(word)
            idfi = vocFrqInv[vocIndex]
        else:
            idfi = 0

        num = (0.5+0.5*freqNormQ[i])*float(idfi)
        wijQ.append(num)

    #calcule normal del vector q.
    normaVecQ = []

    for i in range (0, len(wijQ)):
        norma = wijQ[i] * wijQ[i]
        normaVecQ.append(norma)

    guardePesosQ(vecConsulta, wijQ)

    #calcule s(wix)

    wix = 0
    for i in range(0, len(normaVecQ)):
        wix = wix + normaVecQ[i]

    wix2 = math.sqrt(wix)
    print(wix2)


def guardePesosQ(vecConsulta, wijQ):
    cur_path = os.path.dirname(__file__)
    file_name = cur_path + "/plain_text/" + "pesosQ.txt"
    file_text = open(file_name, '+w', encoding="utf-8")
    for k in range(0, len(vecConsulta)):
        print(str(vecConsulta[k]) + " "+ str(wijQ[k]) )
        file_text.writelines(str(vecConsulta[k]) + "   " + str(wijQ[k]) + "\n")
    file_text.close()


run()


