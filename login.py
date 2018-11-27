from flask import Flask, redirect, url_for, request
app = Flask(__name__)
listURL = []
htmlhead = r'<html> <head> <style>.divider{ width:5px; height:auto; display:inline-block;}</style></head> <body style="background-color:powderblue;">'
htmlString = r'<form action="/newsearch" method="post"><center><p>Escriba su consulta:<input type = "text" name = "nm" /><input type = "submit" value = "Buscar" /></p></center></form>'
htmlbr = "<br>"
botonNext = r'<form action="/newPage" method="post"><button type="submit" name="Siguiente" value="Next">Siguiente</button> </form>'
botonPrev = r'<form action="/oldPage" method="post"><button type="submit" name="Previo" value="Prev">Previo</button></form><div class="divider"/>'
htmlend = r'</body></html>'
numPos = -1
consulta=" "




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
    while i <= x and i < len(listURL):
        strrespon += listURL[i]
        strrespon += htmlbr
        i += 1
    strrespon +=htmlend
    strrespon += botonPrev
    strrespon +=botonNext
    return strrespon
	
	
@app.route('/newPage',methods = ['POST', 'GET'])
def changePageN():
    if request.method == 'POST':
			t=int(numPos)+1
			if (t * 10)<(len(listURL)+10):
				return redirect(url_for('success',name = consulta,y=t))
			else:
				return redirect(url_for('success',name = consulta,y=t-1))

			
@app.route('/oldPage',methods = ['POST', 'GET'])
def changePageO():
    if request.method == 'POST':
			t=int(numPos)-1
			if t>=0:
				return redirect(url_for('success',name = consulta,y=t))
			else:
				return redirect(url_for('success',name = consulta,y=t+1))

			

def fillList():
    for x in range(0, 14):
        temp = r'<a href="https://www.w3schools.com/html/">'+str(x)+r'</a> '
        listURL.append(temp)

		
@app.route('/newsearch',methods = ['POST', 'GET'])
def newlogin():
    if request.method == 'POST':
        fillList()
        user = request.form['nm']
        return redirect(url_for('success',name = user,y=0))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user,y=0))

		

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        fillList()
        user = request.form['nm']
        return redirect(url_for('success',name = user,y=0))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user,y=0))


if __name__ == '__main__':
    app.run(debug = True)