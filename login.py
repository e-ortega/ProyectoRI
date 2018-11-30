from flask import Flask, redirect, url_for, request, render_template
import math
import Etapa2

app = Flask(__name__)
listURL = []
ulrs_dict = {"": ""}
numPos = 0
consulta = " "
cantidad_paginas = 0


@app.route('/page', methods=['POST'])
def change_page():
    if request.method == 'POST':
        global numPos
        if request.form['page_button'] == 'next':

            t = int(numPos) + 1
            numPos = t
            if (t * 10) < (len(listURL) ):
                return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=t,
                                       cantidad_paginas=cantidad_paginas, results=listURL)
            else:
                t = int(numPos) - 1
                numPos = t
                return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=t,
                                       cantidad_paginas=cantidad_paginas, results=listURL)
        elif request.form['page_button'] == 'prev':

            t = int(numPos)
            if t > 0:
                t = int(numPos) - 1
                numPos = t
                return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=t,
                                       cantidad_paginas=cantidad_paginas, results=listURL)
            else:
                numPos = t
                return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=t,
                                       cantidad_paginas=cantidad_paginas, results=listURL)



@app.route('/newPage', methods=['POST', 'GET'])
def changePageN():
    if request.method == 'POST':
        t = int(numPos) + 1
        if (t * 10) < (len(listURL) + 10):
            return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=t,
                                   cantidad_paginas=cantidad_paginas,  results=listURL)
            # return render_template('t.html', name=consulta, y=t, l=listURL)
        else:
            return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=t - 1,
                                   cantidad_paginas=cantidad_paginas,  results=listURL)
            # return render_template('t.html', name=consulta, y=t-1, l=listURL)


@app.route('/oldPage', methods=['POST', 'GET'])
def changePageO():
    if request.method == 'POST':
        t = int(numPos)
        if t >= 0:
            return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=t,
                                   cantidad_paginas=cantidad_paginas, results=listURL)
            # return render_template('t.html', name=consulta, y=t, l=listURL)
        else:
            return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=t + 1,
                                   cantidad_paginas=cantidad_paginas,  results=listURL)
            # return render_template('t.html', name=consulta, y=t+1, l=listURL)


def fillList():

    for x in range(0, 31):
        ulrs_dict[str(x)] = r'<a href="https://www.w3schools.com/html/">' + str(x) + r'</a> '
        temp = r'<a href="https://www.w3schools.com/html/">' + str(x) + r'</a> '
        listURL.append(temp)
    global cantidad_paginas
    cantidad_paginas = math.ceil(len(listURL)/10)


@app.route('/search', methods=['POST'])
def index():
    if request.form['page_button'] == 'prev' or request.form['page_button'] == 'next':
        return change_page()
    else:
        consulta = request.form['searchText']
        if request.method == 'POST':
            listaDocumentos = Etapa2.procesa_consulta(consulta)
            print("sd")

        found_names = []
        for found_name in listaDocumentos:
            found_names.append(found_name[0].replace(".wtd", ""))

        urls = []

        file_name = "URLS.txt"
        file = open(file_name, "r", encoding="utf-8")
        for line in file:
            separator = line.split()
            name = str(separator[0])
            url = str(separator[1])
            name = name.replace(".html","")
            for n in found_names:
                if str(n) == str(name):
                    urls.append(url)
                    break
            
            return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=numPos,
                            cantidad_paginas=cantidad_paginas, results=urls)


@app.route('/')
def main():
    global numPos, listURL
    numPos = 0
    listURL = []
    fillList()
    return render_template('index.html', filename='./static/css/main.css', v=0.01, name="", y=numPos,
                           cantidad_paginas=cantidad_paginas, results=listURL)


if __name__ == '__main__':
    app.run(debug=True)
