from flask import Flask, redirect, url_for, request
app = Flask(__name__)


@app.route('/success/<name>')
def success(name):
    #return 'welcome %s' % name
    str2 = r'<p>Escriba su consulta:<input type = "text" name = "nm" /><input type = "submit" value = "Buscar" /></p>'
    str3 = r'<a href="https://www.w3schools.com/html/">Visit our HTML tutorial</a> ' + "<br>" + r'<a href="https://www.w3schools.com/html/">Visit our HTML tutorial</a> '
    str2 = str2 + str3
    return str2


@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success',name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user))


if __name__ == '__main__':
    app.run(debug = True)