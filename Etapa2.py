import requests
from fractions import Fraction
from bs4 import BeautifulSoup


#este es el vector de palabras que se llena con palabras que se deben omitir en los textos
stop_words = []


#llena el vector stop_words usando la  lista de palabras que se deben omitir
def fillStopWords():
    filename = "stopwords.txt"
    file = open(filename, 'r')
    for line in file:
        stop_words.append(line)


#lee de un archivo y debe substraer el url al que se quiere ingresar y el nombre del archivo
def readFile():
    filename = "ejemplo.txt"
    file = open(filename, "r")
    counter = 0
    separator = []
    for line in file:
        for word in line.split():
            separator.append(word)
            counter += 1
        htmlParser(separator)



#substrae el texto de un html y lo guarda en un archivo
def htmlParser(separator):
    print(separator[1])
    page = requests.get(separator[1])
    name = separator[0]
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.get_text()
    fulltext = name + '.txt'
    fileText = open(fulltext, '+w')
    fileText.write(text)
    fileText.close()

#crea vectores con las frecuencias relativas de los terminos de un documneto
def FreNormal(nombrearchivo, listapalabras, listafrecuencias):
    vectorfecnormal = []
    frecmax = max(listafrecuencias)
    for frec in listafrecuencias:
        valornormal = frec / frecmax
        vectorfecnormal.append(valornormal)
	crearTOK(nombrearchivo, listapalabras,vectorfecnormal)

#crea un archivo .tok a partir de los vectores de palabras y frecuencias normalizadas	
def crearTOK(nombrearchivo, listapalabras, listafrecnormal)
	fulltext = nombrearchivo + '.tok'
	fileText = open(fulltext, '+w')
	vectorStr=[str(i) for i in listafrecnormal]
	int =0
	for i in listapalabras:
		fileText.write(listapalabras[int]+"  "+vectorStr[int] +"\n" )
		int=int+1
	fileText.close()
	
fillStopWords()

#readFile()