import requests
from bs4 import BeautifulSoup

#
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


def htmlParser(separator):
    print(separator[1])
    page = requests.get(separator[1])
    name = separator[0]
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.get_text()
    fulltext = name + '.txt'
    fileText = open(fulltok, '+w')
    fileText.write(text)
    fileText.close()


readFile()