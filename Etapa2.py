#!/usr/bin/python
# -*- coding: utf-8 -*-
import operator
import os
import re
import math
import requests
from os import walk
from http import HTTPStatus
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import namedtuple


# este es el vector de palabras que se llena con palabras que se deben omitir en los textos
plain_text_dir = "plain_text"
posting_file = ""
path = os.path.dirname(os.path.realpath(__file__))
global_words_list = []
stop_words = []
total_frequency_list = []
document_quantity_list = []
# requests_errors = []
tok_path = ""
pesos_documentos = {" ": float}
archivoConsulta={" ":float}
dict = {"": []}
vec_consulta = []
wijQ = []
wix2 = 0
total_docs_procesados = 0


def run():
    # create your subdirectory
    if not os.path.exists(os.path.join(path, plain_text_dir)):
        os.mkdir(os.path.join(path, plain_text_dir))

    fill_stop_words()
    read_urls()
    create_vocabulary()
    calcule_peso()
    indice(r"\posting.txt")

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
    file_dir = os.path.dirname(__file__)

    abs_file_path = file_dir + "/Coleccion" + '/' + name
    page = open(abs_file_path, 'r', encoding="utf-8")
    print("Parseando :" + name)
    soup = BeautifulSoup(page, 'html.parser')
    text = soup.findAll(text=True)
    visible_texts = filter(tag_visible, text)
    clean_text = u" ".join(t.strip() for t in visible_texts)

    tokenizer(clean_text, name)
    # path_file = os.path.join(path, plain_text_dir, file_name)
    # create an empty file.
    # try:
    #     file_text = open(path_file, '+w', encoding="utf-8")
    #     file_text.write(texts)
    #     file_text.close()
    #     tokenizer(path_file)
    # except IOError:
    #     print("Algo pasó creando el archivo el documento: [%s].", file_name)


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


# lee el archivo sin bloques html dado por htmlParser, recorre cada palabra, la busca en stop_words, si no la encuentra
# la busca en el vector de palabras, si la encuentra le suma 1 en la posicion de caso contrario la agrega con un 1
def tokenizer(clean_text, file_name):

    global total_docs_procesados
    total_docs_procesados = total_docs_procesados + 1

    word_list = []
    frequency_list = []
    # file = open(file_name, "r", encoding="utf-8")

    # for line in file:
    for word in clean_text.split():
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
            # requests_errors.append(file_name)
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


# crea un archivo .tok a partir de los vectores de palabras y frecuencias normalizadas
def create_tok(file_name, word_list, normalized_frequency_list, frequency_list):
    # global tok_path
    tok_path = r'.\plain_text\tok'
    if not os.path.exists(tok_path):
        os.makedirs(tok_path)
    file_name = file_name + '.tok'
    file_name = file_name.replace(".html", "")
    index = file_name.find('plain_text')
    file = tok_path + "\\" +file_name

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
            file_text.write(word + " " * (30 - len(word)) + ", " + vector_str[counter] + " " + " " * (
                    12 - len(vector_str[counter])) + " , " + vector_frequency[counter] + " " * (
                                    20 - len(vector_frequency[counter])) + "\n")
            counter += 1
        file_text.close()
    except IOError:
        print("Algo pasó creando el .tok para el documento: [%s].", file_name)


# Hace un sort para 3 lista, tomando como ordenamiento la lista base, este algorito es utilizado para ordenar el vocabulario
def merge_sort_3_listas(lista_base, lista1, lista2):
    if len(lista_base) > 1:
        medio = len(lista_base) // 2
        mitad_iz_base = lista_base[:medio]
        mitad_de_base = lista_base[medio:]

        mitad_iz1 = lista1[:medio]
        mitad_de1 = lista1[medio:]

        mitad_iz2 = lista2[:medio]
        mitad_de2 = lista2[medio:]

        merge_sort_3_listas(mitad_iz_base, mitad_iz1, mitad_iz2)
        merge_sort_3_listas(mitad_de_base, mitad_de1, mitad_de2)

        i = 0
        j = 0
        k = 0

        while i < len(mitad_iz_base) and j < len(mitad_de_base):
            if mitad_iz_base[i] < mitad_de_base[j]:
                lista_base[k] = mitad_iz_base[i]
                lista1[k] = mitad_iz1[i]
                lista2[k] = mitad_iz2[i]
                i = i + 1
            else:
                lista_base[k] = mitad_de_base[j]
                lista1[k] = mitad_de1[j]
                lista2[k] = mitad_de2[j]
                j = j + 1
            k = k + 1

        while i < len(mitad_iz_base):
            lista_base[k] = mitad_iz_base[i]
            lista1[k] = mitad_iz1[i]
            lista2[k] = mitad_iz2[i]
            i = i + 1
            k = k + 1

        while j < len(mitad_de_base):
            lista_base[k] = mitad_de_base[j]
            lista1[k] = mitad_de1[j]
            lista2[k] = mitad_de2[j]
            j = j + 1
            k = k + 1


# crea el archivo vabulario
def create_vocabulary():
    file_name = 'Vocabulario.txt'
    file_name = os.path.join(path, plain_text_dir, file_name)

    merge_sort_3_listas(global_words_list, total_frequency_list, document_quantity_list)

    # termino,  # doc diferentes en que aparece el termino, frecuencia inversa(idf)
    # idf = log(total_doc /  # docs en termino)
    #         log()

    vector_frequency = []
    try:
        file_text = open(file_name, '+w', encoding="utf-8")
        for freq in document_quantity_list:
            value = math.log(total_docs_procesados / freq, 10)
            vector_frequency.append(str(value))

        # vector_frequency = [str(i) for i in total_frequency_list]
        vector_quantity = [str(i) for i in document_quantity_list]
        counter = 0
        for word in global_words_list:
            file_text.write(str(word) + " " + ", " + str(vector_quantity[counter]) + " " + ", " + str(vector_frequency[counter]) + "\n")
            counter += 1
        file_text.close()
    except IOError:
        print("Algo pasó creando el .tok para el documento: [%s].", file_name)
    print("d")

# Crea in Indice a partir del archivo posting
def indice(archivo):
    archivo = archivo.replace(".\\", "\\")
    file_name = 'Indice.txt'
    file_name = os.path.join(path, plain_text_dir, file_name)
    # resultado = os.path.join(path, plain_text_dir, archivo)
    resultado = file_name.replace("\\Indice.txt", archivo)
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
        # probar al contrario
        pos = l.find(" ")
        #pos = l.find(",")
        lines[c] = l[:pos]
        c = c + 1
    termino = " "
    c = 0
    try:
        file_text = open(file_name, '+w', encoding="utf-8")
        unique = set(lines)
        unique = sorted(unique)
        for termino in unique:
            numeroVeces = lines.count(termino)
            primera_pos = lines.index(termino)
            file_text.write(termino + " " * (30 - len(termino)) + ", " + str(primera_pos) + " " * (12 - len(str(primera_pos))) + ", " + str(
                numeroVeces) + "\n")

        file_text.close()
        print("")

    except IOError:
        print("Algo pasó creando el archivo Indice")


def calcula_pesos(frecuencia_normalizada, frecuencia_inversa):
    return frecuencia_normalizada * frecuencia_inversa


def load_vocabulario(palabras, frecuencias):
    # file_name = 'vocabulario.txt'
    cur_path = os.path.dirname(__file__)
    a = cur_path + '/plain_text/Vocabulario.txt'
    # a = 'C:/Users/Jose M/Google Drive/II Semestre 2018/Proyecto/plain_text/Vocabulario.txt'
    with open(a, 'r', encoding="utf-8") as file:
        for line in file:
            terminos = line.split()

            palabras.append(terminos[0])
            frecuencias.append(terminos[4])



def calcule_peso():
    palabras = []
    idfs = []
    palabras_tok = []
    frecuencias_tok = [] # freq normalizadas
    palabra_peso = []
    pesos = []
    load_vocabulario(palabras, idfs)
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
    for n in range(0, len(f)):

        file_name = tok_path + "/" + f[n]
        print("creando tok %s", file_name)
        file = open(file_name, 'r', encoding="utf-8")
        for line in file:
            word_count = 0
            for word in line.split():
                if word_count == 0:
                    palabras_tok.append(word)
                    word_count = word_count + 1
                elif word_count == 2:
                    frecuencias_tok.append(word)
                    word_count = word_count + 1
                else:
                    word_count = word_count + 1
        for i in range(0, len(palabras_tok)):
            for j in range(0, len(palabras)):
                if palabras[j] == palabras_tok[i]:
                    palabra_peso.append(palabras_tok[i])
                    pesos.append(float(frecuencias_tok[i]) * float(idfs[j]))
        file_name = cur_path + "/plain_text/wtd/" + f[n] + ".wtd"
        file_name = file_name.replace(".tok", "")
        file_text = open(file_name, '+w', encoding="utf-8")
        for k in range(0, len(palabra_peso)):
            file_text.writelines(str(palabra_peso[k]) + "   " + str(pesos[k]) + "\n")
            file_posting.writelines(str(palabra_peso[k]) + "   " + f[n].replace(".txt.tok", "") + "   " + str(pesos[k]) + "\n")
        file_text.close()
        palabras_tok = []
        frecuencias_tok = []
        palabra_peso = []
        pesos = []
    file_posting.close()
    global posting_file
    posting_file = dir_path_posting
    input_file = open(dir_path_posting, 'r', encoding="utf-8")
    line_list = input_file.readlines()
    input_file.close()
    line_list.sort()
    with open(dir_path_posting, 'w', encoding="utf-8") as f:
        for line in line_list:
            f.write(line)


def procesa_consulta(consulta):
    consulta_cont = []
    global dict
    dict = {"": []}
    dict.clear()
    words = consulta.split()
    global vec_consulta
    vec_consulta = []
    # en esta parte solo saca palabras y calcula  la frecuencia(freqij)
    for word in words:
        word = word.lower()
        if stop_words.__contains__(word):
            print("something")
        else:
            if not vec_consulta.__contains__(word):
                vec_consulta.append(word)
                consulta_cont.append(1)
            else:
                if(len(vec_consulta)) >0:
                    index = vec_consulta.index(word)
                    consulta_cont[index] = consulta_cont[index] + 1

    # calcula freq normalizada(tfij)

    maximo_index = max(consulta_cont)
    freq_norm_q = []

    for i in range(0, len(consulta_cont)):
        freq_norm_q .append(consulta_cont[i]/maximo_index)


    # Cargue Vocabulario
    cur_path = os.path.dirname(__file__)
    voc_palabras = []
    voc_num_ter = []
    voc_frq_inv = []

    file_name = cur_path + "/plain_text/Vocabulario.txt"
    file = open(file_name, 'r', encoding="utf-8")

    for line in file:
        count = 0
        for entry in line.split():
            if count == 0:
                voc_palabras.append(entry)
                count = count + 1
            elif count == 2:
                voc_num_ter.append(entry)
                count = count + 1
            elif count == 4:
                voc_frq_inv.append(entry)
                count = count + 1
            else:
                count = count + 1
    # calcule pesos(wij)

    print("paso")

    for i in range(0, len(freq_norm_q)):
        word = vec_consulta[i]

        if voc_palabras.__contains__(word):
            voc_index = voc_palabras.index(word)
            idfi = voc_frq_inv[voc_index]
        else:
            idfi = 0

        num = (0.5+0.5*freq_norm_q[i])*float(idfi)
        wijQ.append(num)

    for vec in vec_consulta:
        calcule_producto_punto(vec)

    # calcule normal del vector q.
    norma_vec_q = []

    for i in range (0, len(wijQ)):
        norma = wijQ[i] * wijQ[i]
        norma_vec_q.append(norma)

    guarde_pesos_q(vec_consulta, wijQ)

    # calcule s(wix)

    wix = 0
    for i in range(0, len(norma_vec_q)):
        wix = wix + norma_vec_q[i]

    global wix2
    wix2 = math.sqrt(wix)
    print(wix2)

    return sume_dict()




def calcule_producto_punto(vec):

    #Abre el archivo postings  y lo carga
    cur_path = os.path.dirname(__file__)
    post_palabras = []
    post_archivo = []
    post_peso = []
    indexes= []
    file_name = cur_path + "/plain_text/posting.txt"
    file = open(file_name, 'r', encoding="utf-8")

    indexes = file.read()
    first = indexes.find(vec)
    last = indexes.rfind(vec)
    if first < last:
        first_jump = indexes.find("\n", last)
        sublist = indexes[first : first_jump].split("\n")
    else:
        first_jump = indexes.find("\n", first)
        sublist = indexes[first: first_jump].split("\n")
    index = vec_consulta.index(vec)
    global weight
    weight = wijQ[index]
    global dict

    for line in sublist:
        values = line.split()
        if values != []:
            print (values[0] + " "+ values[1]+ " "+values[2])
            values[1] = values[1].replace("tok", "wtd")
            if values[1] in dict :
                new_list = []
                new_list = dict[values[1]]
                new_list.append(float(values[2])*weight)
                dict[values[1]] = new_list
            else:
                temp = []
                temp.append(float(values[2])*weight)
                dict[values[1]] = temp

    file.close()



def sume_dict():
    temp = []
    global dict
    for item in dict:
        sum = 0
        list = dict[item]
        for j in range (0, len(list)):
            sum = sum + float(list[j])
        dict[item] = sum

    return similitud(r"\plain_text\pesosQ.txt")



def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs




def guarde_pesos_q(vec_consulta, wijQ):
    cur_path = os.path.dirname(__file__)
    file_name = cur_path + "/plain_text/" + "pesosQ.txt"
    file_text = open(file_name, '+w', encoding="utf-8")
    for k in range(0, len(vec_consulta)):
        print(str(vec_consulta[k]) + " " + str(wijQ[k]))
        file_text.writelines(str(vec_consulta[k]) + "   " + str(wijQ[k]) + "\n")
    file_text.close()


# Analiza la similitud de archivos
def similitud(archivo):
    global pesos_documentos
    pesos_documentos = {"": float}
    pesos_documentos.clear()
    listaFileConsulta=[]
    archivo = archivo.replace(".\\", "\\")
    file_name = 'pesosQ.txt'
    file_name = os.path.join(path, plain_text_dir, file_name)
    # resultado = os.path.join(path, plain_text_dir, archivo)
    resultado = file_name.replace("\\plain_text\\pesosQ.txt", archivo)
    print(resultado)
    try:
        lines = []
        pesosCon = []
        with open(resultado, encoding="utf8") as file:
            for line in file:
                line = line.strip()
                lines.append(line)
    except Exception as e:
        print(e)
    c = 0
    for l in lines:
        # probar al contrario
        pos = l.find(" ")
        #pos = l.find(",")
        lines[c] = l[:pos]
        pesosCon.append(l[pos:])
        c = c + 1
        #r"\plain_text\pesosQ.txt"
    archivo2 = r"\plain_text\Indice.txt"
    archivo2 = archivo2.replace(".\\", "\\")
    file_name2 = 'Indice.txt'
    file_name2 = os.path.join(path, plain_text_dir, file_name2)
    # resultado = os.path.join(path, plain_text_dir, archivo)
    resultado2 = file_name2.replace("\\plain_text\\Indice.txt", archivo2)
    try:
        lines2 = []
        with open(resultado2, encoding="utf8") as file2:
            for line in file2:
                line = line.strip()
                lines2.append(line)
    except Exception as e:
        print(e)
    archivo3 = r"\plain_text\Posting.txt"
    archivo3 = archivo3.replace(".\\", "\\")
    file_name3 = 'Posting.txt'
    file_name3 = os.path.join(path, plain_text_dir, file_name3)
    # resultado = os.path.join(path, plain_text_dir, archivo)
    resultado3 = file_name3.replace("\\plain_text\\Posting.txt", archivo3)
    try:
        lines3 = []
        with open(resultado3, encoding="utf8") as file3:
            for line in file3:
                line = line.strip()
                lines3.append(line)
    except Exception as e:
        print(e)
    for l in lines:
        temp=0
        for IndiceLine in lines2:
            count = 0
            for entry in IndiceLine.split():
                if count == 0:
                    I1 = entry # palabra del indice
                    count = count + 1
                elif count == 2:
                    I2 = entry # posicion palabra en posting
                    count = count + 1
                elif count == 4:
                    I3 = entry # numero veces palabra en posting
                    count = count + 1
                else:
                    count = count + 1

            if l == I1:
                P1 = I2
                for x in range(int(I3)):
                    listaFileConsulta.append(lines3[int(P1) + x])
    for l in listaFileConsulta:
        global archivoConsulta


        archivoConsulta = l[l.find(" "):l.rfind(" ")]
        archivoConsulta = archivoConsulta.replace(" ", "")
        cur_path = os.path.dirname(__file__)
        archivoConsulta = archivoConsulta.replace(".tok", ".wtd")
        file_consulta = cur_path + "/plain_text/wtd/" + archivoConsulta
        resultadoConsulta = file_consulta.replace("\\plain_text\\wtd\\"+archivoConsulta, archivoConsulta)
        try:
            lines3 = []
            with open(resultadoConsulta, encoding="utf8") as file3:
                for line in file3:
                    line = line.strip()
                    lines3.append(line)
        except Exception as e:
            print(e)
        sumaPeso=0
        for l in lines3:
            cuadrado=float((l[l.find(" "):]))**2
            sumaPeso += cuadrado

        valorF=sumaPeso**0.5
        pesos_documentos[archivoConsulta]=valorF
    return calculo_similitud()



#vec1 va a ser el nombre del documento y vec2 va a ser el valor
def calculo_similitud():
    global pesos_documentos
    global dict
    global wix2
    ranking = {"": int}
    ranking.clear()
    for key, values in pesos_documentos.items():
        if key.strip():
            producto_punto_Q = dict[key]
            producto_punto_doc = pesos_documentos[key]
            if producto_punto_Q != 0 and wix2 != 0:
                similitud_doc = float(producto_punto_doc) / (float(producto_punto_Q)*float(wix2))
            else:
                similitud_doc = float(producto_punto_doc)
            ranking[key] = similitud_doc
            print("Similitud del doc es: " + str(similitud_doc))

    sorted_d = sorted(ranking.items(), key=lambda x: x[1])

    list_archivos = []
    for tuples in sorted_d:
        archivo = tuples[0]
        archivo = archivo.replace(".wtd", ".html")
        list_archivos.append(archivo)

    file_name = "urles.txt"
    file = open(file_name, "r", encoding="utf-8")
    list_urls = []
    lineas_todo = []
    for line in file:
        lineas = line.split()
        lineas_todo.append(lineas)

    for archivo in list_archivos:
        for linea in lineas_todo:
            if archivo == linea[0]:
                temp = r'<a href="'+linea[1]+'">' + str(linea[0]) + r'</a> '
                list_urls.append(temp)
                break
    return list_urls


run()


