from flask import Flask, redirect, url_for, request
app = Flask(__name__)
listURL = []
htmlString = r'<p>Escriba su consulta:<input type = "text" name = "nm" /><input type = "submit" value = "Buscar" /></p>'
htmlbr = "<br>"
numPos = 1



@app.route('/success/<name>')
def success(name):
    #return 'welcome %s' % name
    #str2 = r'<p>Escriba su consulta:<input type = "text" name = "nm" /><input type = "submit" value = "Buscar" /></p>'
    #str3 = r'<a href="https://www.w3schools.com/html/">Visit our HTML tutorial</a> ' + "<br>" + r'<a href="https://www.w3schools.com/html/">Visit our HTML tutorial</a> '
    strrespon = htmlString
    i= 9*numPos-9
    for x in range(i, 9*numPos):
        strrespon += listURL[i]
        strrespon += htmlbr
    numberPos = numPos+10
    return strrespon


def fillList():
    for x in range(0, 14):
        temp = r'<a href="https://www.w3schools.com/html/">'+str(x)+r'</a> '
        listURL.append(temp)


@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        fillList()
        user = request.form['nm']
        return redirect(url_for('success',name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user))


if __name__ == '__main__':
    app.run(debug = True)