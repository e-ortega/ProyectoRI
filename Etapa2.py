#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import requests
from http import HTTPStatus
from bs4 import BeautifulSoup
from bs4.element import Comment

# este es el vector de palabras que se llena con palabras que se deben omitir en los textos
stop_words = []
plain_text_dir = "plain_text"
path = os.path.dirname(os.path.realpath(__file__))
global_words_list = []
total_frequency_list = []
document_quantity_list = []
requests_errors = []


def run():
    # create your subdirectory
    if not os.path.exists(os.path.join(path, plain_text_dir)):
        os.mkdir(os.path.join(path, plain_text_dir))

    fill_stop_words()
    read_urls()
    generate_error_page_file()


# llena el vector stop_words usando la  lista de palabras que se deben omitir
def fill_stop_words():
    file_name = "stopwords.txt"
    file = open(file_name, 'r', encoding="utf-8")
    for line in file:
        for word in line.split():  # para que no salga el \n
            stop_words.append(word)


# lee de un archivo y debe substraer el url al que se quiere ingresar y el nombre del archivo
def read_urls():
    file_name = "URLS.txt"
    file = open(file_name, "r", encoding="utf-8")
    for line in file:
        separator = []
        for word in line.split():
            separator.append(word)
        html_parser(separator)


# substrae el texto de un html y lo guarda en un archivo
def html_parser(separator):
    name = separator[0]
    file_name = name + '.txt'
    try:
        page = requests.get(separator[1])
        if page.status_code == HTTPStatus.OK:
            soup = BeautifulSoup(page.content, 'html.parser')
            text = soup.findAll(text=True)
            visible_texts = filter(tag_visible, text)
            texts = u" ".join(t.strip() for t in visible_texts)
            #  print("Procesando archivo " + file_name)
            path_file = os.path.join(path, plain_text_dir, file_name)

            # create an empty file.
            try:
                file_text = open(path_file, '+w', encoding="utf-8")
                file_text.write(texts)
                file_text.close()
                tokenizer(path_file)
            except IOError:
                print("Algo pasó creando el archivo el documento: [%s].", file_name)
    except requests.exceptions.RequestException as error:
        print(error)
        requests_errors.append(file_name)


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
                    # print("[" + str(word) + "] longitud de palaba no permitida")
                    valid_word = False  # no se usan palabras de tamaño mayor a 30
                if len(word) > 0:
                    if not word.isdigit() and not word[0].isalpha():
                        # print("[" + str(word) + "] no es una palabra valida")
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
    file_name = file_name + '.tok'
    for passnum in range(1,len(word_list)):
      i=0
      for element in range(0,len(word_list)-passnum):
        if (word_list[i]>word_list[i+1]):
          temp = word_list[i]
          word_list[i] = word_list[i+1]
          word_list[i+1] = temp
          temp = normalized_frequency_list[i]
          normalized_frequency_list[i] = normalized_frequency_list[i+1]
          normalized_frequency_list[i+1] = temp
          temp = frequency_list[i]
          frequency_list[i] = frequency_list[i+1]
          frequency_list[i+1] = temp
        i += 1

    try:
        file_text = open(file_name, '+w', encoding="utf-8")
        vector_str = [str(i) for i in normalized_frequency_list]
        vector_frequency = [str(i) for i in frequency_list]
        counter = 0
        for word in word_list:
            #file_text.write(word + "," + vector_str[counter] + "," + vector_frequency[counter] + "\n")
            file_text.write(word+" "*(30-len(word)) + "," + vector_str[counter] +" "*(12-len(vector_str[counter]))+ "," + vector_frequency[counter]+" "*(20-len(vector_frequency[counter])) + "\n")
            counter += 1
        file_text.close()
    except IOError:
        print("Algo pasó creando el .tok para el documento: [%s].", file_name)
# def create_tok(file_name, word_list, normalized_frequency_list, frequency_list):
    # file_name = file_name + '.tok'
	# for passnum in range(len(word_list)-1,0,-1):
          # i=0
          # for element in range(passnum):
            # if word_list[i]>word_list[i+1]:
                # temp = word_list[i]
                # word_list[i] = word_list[i+1]
                # word_list[i+1] = temp
                # temp = normalized_frequency_list[i]
                # normalized_frequency_list[i] = normalized_frequency_list[i+1]
                # normalized_frequency_list[i+1] = temp
                # temp = frequency_list[i]
                # frequency_list[i] = frequency_list[i+1]
                # frequency_list[i+1] = temp
            # i += 1
    # try:
        # file_text = open(file_name, '+w', encoding="utf-8")
        # vector_str = [str(i) for i in normalized_frequency_list]
        # vector_frequency = [str(i) for i in frequency_list]
        # counter = 0
        # for word in word_list:
            # #file_text.write(word + "," + vector_str[counter] + "," + vector_frequency[counter] + "\n")
            # file_text.write(word+" "*(30-len(word)) + "," + vector_str[counter] +" "*(12-len(vector_str[counter]))+ "," + vector_frequency[counter]+" "*(20-len(vector_frequency[counter])) + "\n")
			# counter += 1
        # file_text.close()
    # except IOError:
        # print("Algo pasó creando el .tok para el documento: [%s].", file_name)


# crea el archivo vabulario
def create_vocabulary():
    file_name = 'Vocabulario.txt'
    file_name = os.path.join(path, plain_text_dir, file_name)
    try:
        file_text = open(file_name, '+w', encoding="utf-8")
        vector_frequency = [str(i) for i in total_frequency_list]
        vector_quantity = [str(i) for i in document_quantity_list]
        counter = 0
        for word in global_words_list:
            file_text.write(str(word) + "," + str(vector_frequency[counter]) + "," + str(vector_quantity[counter]) + "\n")
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
    file_name = 'Indice.txt'
    resultado = []
    lines = [line.rstrip('\n') for line in open(archivo)]
    c = 0
    for l in lines:
        pos = l.find(" ")
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
                file_text.write(termino + " " * (30-len(termino)) + "," + str(c) + " " * (12-len(str(c))) + "," + str(numeroVeces)+"\n")
                numeroVeces = 0
          c = c+1
    except IOError:
        print("Algo pasó creando el archivo Indice")


def calculaPesos(frecuenciaNormalizada, frecuenciaInversa):
    return frecuenciaNormalizada * frecuenciaInversa


def loadVocabulario(palabras, frecuencias):
    file_name = 'vocabulario.txt'
    file = open(file_name, 'r', encoding="utf-8")
    for line in file:
        count = 0
        for word in line:
            if count == 0:
                palabras.append(word)
            elif count == 2:
                frecuencias.append(word)
        count = count +1


run()
