from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)
listURL = []
htmlhead = r'<html> <head> <style>footer {background-color: #777;padding: 10px;text-align: center;color: white;}.divider{ width:5px; height:auto; display:inline-block;} article {float: left;padding: 20px;width: 70%;background-color: #08b4fc;height: 300px; }nav {float: left;width: 10%;height: 300px;background: #08b4fc;padding: 20px;}</style></head> <body style="background-color:#08b4fc;">'
htmlString = r'<form action="/newsearch" method="post"><center><p>Escriba su consulta:<input type = "text" name = "nm" /><input type = "submit" value = "Buscar" /></p></center></form>'
htmlSection=r'<section><nav><ul></ul></nav><article>'
numeroRes=r'Numero de resultados :'
htmlbr = "<br>"
botonNext = r'<form action="/newPage" method="post"><button type="submit" name="Siguiente" value="Next">Siguiente</button> </form></footer>'
botonPrev = r'</article></section><section><nav><ul></ul></nav><article><form action="/oldPage" method="post"><button type="submit" name="Previo" value="Prev">Previo</button></article></section>'
htmlend = r'</body></html>'
numPos = -1
consulta=" "
#<img src="./imagen/cloud1.png" alt="Trulli" width="241" height="141">



@app.route('/success/<name>/<y>')
def success(name,y):
    strrespon = htmlhead
    global consulta 
    consulta = name
    strrespon += htmlString
    global numPos
    numPos = int(y)
    x = 9 + numPos * 10
    i = x-9
    strrespon+=htmlSection
    strrespon +=numeroRes + str(len(listURL)) + htmlbr
    while i <= x and i < len(listURL):
        strrespon += listURL[i]
        strrespon += htmlbr + htmlbr
        i += 1
    
    strrespon += botonPrev
    strrespon +=botonNext
    strrespon +=htmlend
    return strrespon
	
	
@app.route('/newPage',methods = ['POST', 'GET'])
def changePageN():
    if request.method == 'POST':
        t=int(numPos)+1
        if (t * 10)<(len(listURL)+10):
            return render_template('t.html', name=consulta, y=t, l=listURL)
        else:
            return render_template('t.html', name=consulta, y=t-1, l=listURL)

			
@app.route('/oldPage',methods = ['POST', 'GET'])
def changePageO():
    if request.method == 'POST':
        t=int(numPos)-1
        if t>=0:
            return render_template('t.html', name=consulta, y=t, l=listURL)
        else:
            return render_template('t.html', name=consulta, y=t+1, l=listURL)

			

def fillList():
    for x in range(0, 14):
        temp = r'<a href="https://www.w3schools.com/html/">'+str(x)+r'</a> '
        listURL.append(temp)

		
@app.route('/newsearch',methods = ['POST', 'GET'])
def newlogin():
    if request.method == 'POST':

        fillList()
        user = request.form['nm']
        return render_template('t.html', name=user, y=0, l=listURL)
    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user,y=0))

		

@app.route('/search',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        fillList()
        consulta = request.form['searchText']
        return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=0, l=listURL)
        #return render_template('t.html',name = user,y=0,l=listURL)
		#return redirect(url_for('success',name = user,y=0))
    else:
        user = request.args.get('searchText')
        #return redirect(url_for('success',name = user,y=0))
        #return render_template('t.html')
        return render_template('index.html', filename='./static/css/main.css', v=0.01, name=consulta, y=0, l=listURL)

@app.route('/')
def main():
		return render_template('index.html',filename='./static/css/main.css', v=0.01,name = "",y=0,l=listURL)

if __name__ == '__main__':
    app.run(debug = True)