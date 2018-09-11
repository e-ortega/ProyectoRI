import requests
from bs4 import BeautifulSoup

stop_words = []

def fillStopWords():
    filename = "stopwords.txt"
    file = open(filename, 'r')
    for line in file:
        stop_words.append(line)


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
    fileText = open(fulltext, '+w')
    fileText.write(text)
    fileText.close()


fillStopWords()

#readFile()