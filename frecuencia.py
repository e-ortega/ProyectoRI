from fractions import Fraction

def FreNormal(listapalabras, listafrecuencias):
    vectorfecnormal = []
    frecmax = max(listafrecuencias)
    for frec in listafrecuencias:
        print('Fre ',  frec,' Fmax ', frecmax)
        valornormal = frec / frecmax#Fraction(frec, frecmax)
        print(valornormal)
        vectorfecnormal.append(valornormal)
    print vectorfecnormal



lista = [10, 15, 79, 45, 314, 54, 54, 47]
list1 = []
for item in lista:
    print item
FreNormal(list1, lista)


