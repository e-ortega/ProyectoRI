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


def run():
    # create your subdirectory
    if not os.path.exists(os.path.join(path, plain_text_dir)):
        os.mkdir(os.path.join(path, plain_text_dir))

    fill_stop_words()
    read_urls()


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
    name = separator[0]
    page = requests.get(separator[1])

    if page.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.findAll(text=True)
        visible_texts = filter(tag_visible, text)
        texts = u" ".join(t.strip() for t in visible_texts)

        file_name = name + '.txt'
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
                if word=="中文":
                    print("d")
                valid_word = True
                word = word.lower()
                word = re.sub(r'\W+', '', word)  # se eliminan caracteres no alfanumericos
                if not word.isalnum():
                    valid_word = False
                if len(word) < 2 or len(word) > 30:
                    print("[%s] longitud de palaba no permitida" % word)
                    valid_word = False  # no se usan palabras de tamaño mayor a 30
                if not word.isdigit() and not word[0].isalpha():
                    print("[%s] no es una palabra valida" % word)
                    valid_word = False# no se usan palabras que no sean solo numeros y no empiecen por a-z ej: 3arbol

                if not stop_words.__contains__(word) and valid_word:
                    if word_list.__contains__(word):
                        frequency_list[word_list.index(word)] += 1
                    else:
                        word_list.append(word)
                        frequency_list.append(1)
            except Exception as error:
                print("[%s] %s" % (word, error))
                print(error)
    normalize_frequency(file_name, word_list, frequency_list)


# crea vectores con las frecuencias relativas de los terminos de un documneto
def normalize_frequency(file_name, word_list, frequency_list):
    normalized_frequency_list = []
    max_frequency = max(frequency_list)
    for frequency in frequency_list:
        normalized_value = frequency / max_frequency
        normalized_frequency_list.append(normalized_value)
    create_tok(file_name, word_list, normalized_frequency_list, frequency_list)


# crea un archivo .tok a partir de los vectores de palabras y frecuencias normalizadas
def create_tok(file_name, word_list, normalized_frequency_list, frequency_list):
    fulltext = file_name + '.tok'

    try:
        file_text = open(fulltext, '+w', encoding="utf-8")
        vector_str = [str(i) for i in normalized_frequency_list]
        vector_frequency = [str(i) for i in frequency_list]
        counter = 0
        for word in word_list:
            file_text.write(word + "  " + vector_str[counter] + "   " + vector_frequency[counter] + "\n")
            counter += 1
        file_text.close()
    except IOError:
        print("Algo pasó creando el .tok para el documento: [%s].", file_name)


# crea el archivo vabulario
def create_vocabulary():
    print("TO-DO")


run()
