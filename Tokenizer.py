#este es el vector de palabras que se llena con palabras que se deben omitir en los textos
stop_words = []


#llena el vector stop_words usando la  lista de palabras que se deben omitir
def fillStopWords():
    filename = "stopwords.txt"
    file = open(filename, 'r')
    for line in file:
        for word in line.split():
            stop_words.append(word)

def tokenizer(archivo):
    listapalabras = []
    listafrecuencias = []
    filename = archivo
    file = open(filename, "r")
    for line in file:
        for word in line.split():
            if (not stop_words.__contains__(word)):
                if (listapalabras.__contains__(word)):
                    listafrecuencias[listapalabras.index(word)] += 1
                else:
                    listapalabras.append(word)
                    listafrecuencias.append(1)
    #i = 0
    #for j in listapalabras:
    #    print(listapalabras[i] + " " + str(listafrecuencias[i]))
    #    i += 1
    #FreNormal(archivo, listapalabras, listafrecuencias)


fillStopWords()
print(stop_words)
tokenizer("EjemploPalabras.txt")

