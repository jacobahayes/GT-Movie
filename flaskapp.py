import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/nowplaying")
def nowplaying():
    return render_template("nowplaying.html")

@app.route("/me")
def me():
    return render_template("me.html")

@app.route("/movie")
def movie():
    return render_template("movie.html")

@app.route("/overview")
def overview():
    return render_template("overview.html")

@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/givereview")
def give_review():
    return render_template("givereview.html")

@app.route("/choosetheater", methods=['GET', 'POST'])
def choose_theater():
    if request.method == 'GET':
        return render_template("choosetheater.html")
    if request.method == 'POST':
        try:
            theater = request.form['Choose']
            #return render_template("selecttime.html") 
            return redirect("/selecttime/" + theater)
        except:
            search = request.form['Search']
            return redirect("/theaterresults/" + search)

@app.route("/theaterresults/<keyword>", methods=['GET', 'POST'])
def theaterresults(keyword):
    if request.method == 'GET':
        #do stuff with keyword
        return render_template("theaterresults.html")
    if request.method == 'POST':
        #Do query with keyword
        theater = request.form['theater']
        try:
            saveTheater = request.form['saveTheater']
            if (saveTheater == 'check'):
                #SQL
                print("Save theater")
        except:
            #SQL
            print("Don't save")
        return redirect("/selecttime/" + theater)

@app.route("/selecttime/<theater>", methods=['GET', 'POST'])
def selecttime(theater):
    #Do query with theater
    return render_template("selecttime.html", theater=theater)

if __name__ == '__main__':
    app.run()
