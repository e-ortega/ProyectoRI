from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)
listURL = []
ulrs_dict = {"", ""}
numPos = -1
consulta=" "


@app.route('/newPage',methods = ['POST', 'GET'])
def changePageN():
    if request.method == 'POST':
        t=int(numPos)+1
        if (t * 10)<(len(listURL)+10):
            return render_template('t.html', name=consulta, y=t, l=listURL)
        else:
            return render_template('t.html', name=consulta, y=t-1, l=listURL)


@app.route('/oldPage', methods=['POST', 'GET'])
def changePageO():
    if request.method == 'POST':
        t=int(numPos)-1
        if t>=0:
            return render_template('t.html', name=consulta, y=t, l=listURL)
        else:
            return render_template('t.html', name=consulta, y=t+1, l=listURL)


def fillList():
    for x in range(0, 14):
        ulrs_dict[str(x)] = r'<a href="https://www.w3schools.com/html/"></a>'
        temp = r'<a href="https://www.w3schools.com/html/">'+str(x)+r'</a> '
        listURL.append(temp)


@app.route('/search', methods=['POST'])
def index():
    consulta = request.form['searchText']
    if request.method == 'POST':
        fillList()
        return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=0, results=listURL)


@app.route('/')
def main():
    return render_template('index.html', filename='./static/css/main.css', v=0.01, name="", y=0, urls=ulrs_dict, results=listURL)


if __name__ == '__main__':
    app.run(debug=True)
