#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# este es el vector de palabras que se llena con palabras que se deben omitir en los textos
stop_words = []


def run():
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
    file_name = "URLS.txt"
    file = open(file_name, "r", encoding="utf-8")
    # counter = 0
    separator = []
    for line in file:
        for word in line.split():
            separator.append(word)
            # counter += 1
        html_parser(separator)
    # tokenizer("archivo.txt")


# substrae el texto de un html y lo guarda en un archivo
def html_parser(separator):
    print(separator[1])
    page = requests.get(separator[1])
    name = separator[0]
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.get_text()
    full_text = name + '.txt'
    file_text = open(full_text, '+w', encoding="utf-8")
    file_text.write(text)
    file_text.close()


# lee el archivo sin bloques html dado por htmlParser, recorre cada palabra, la busca en stop_words, si no la encuentra
# la busca en el vector de palabras, si la encuentra le suma 1 en la posicion de caso contrario la agrega con un 1
def tokenizer(filename):
    word_list = []
    frequency_list = []
    # filename = archivo
    file = open(filename, "r", encoding="utf-8")
    for line in file:
        for word in line.split():
            if not stop_words.__contains__(word):
                if word_list.__contains__(word):
                    frequency_list[word_list.index(word)] += 1
                else:
                    word_list.append(word)
                    frequency_list.append(1)
    # i = 0
    # for j in word_list:
    #    print(word_list[i] + " " + str(frequency_list[i]))
    #    i += 1
    normalize_frequency(filename, word_list, frequency_list)


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
    file_text = open(fulltext, '+w', encoding="utf-8")
    vectorStr = [str(i) for i in normalized_frequency_list]
    vectorFrec = [str(i) for i in frequency_list]
    counter = 0
    for i in word_list:
        file_text.write(word_list[counter] + "  " + vectorStr[counter] + "   " + vectorFrec[counter] + "\n")
        counter = counter + 1
        file_text.close()


# crea el archivo vabulario
def create_vocabulary():
    print("TO-DO")


run()
