def main():
    lista = [10, 15, 79, 45, 314, 54, 54, 47]
    list1 = []
    for item in lista:
        print item
    FreNormal(list1, lista)


def FreNormal(listapalabras, listafrecuencias):
    vectorfecnormal = []
    frecmax = max(listafrecuencias)
    for frec in listafrecuencias:
        valornormal = frec/frecmax
        vectorfecnormal.append(valornormal)
    print vectorfecnormal
