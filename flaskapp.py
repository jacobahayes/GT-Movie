import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config.from_pyfile('flaskapp.cfg')
app.config['MYSQL_DATABASE_USER'] = 'admingu2v3JA'
app.config['MYSQL_DATABASE_PASSWORD'] = '4eaeGBP2ZlDh'
app.config['MYSQL_DATABASE_DB'] = 'gtmovie'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        return("okay")
    except Exception as e:
        return(str(e))


    #Query for login
    #if(query returns true) login
    #else tell user they're dumba nd to try again
    #return render_template('index.html')

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
    if request.method == 'GET':
        #Do query with theater
        #Get times
        times = ['1:00pm', '3:00pm', '5:00pm', '7:00pm']
        return render_template("selecttime.html", times=times, theater=theater)
    if request.method == 'POST':
        try:
            time = request.form['showtime']
        except:
            time = 'n/a'
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return render_template("buyticket.html", nums=nums, theater=theater, time=time)

@app.route("/paymentinfo", methods=['GET', 'POST'])                                                        
def paymentinfo():                                                                                     
    try:
        time = request.form['time']
        theater = request.form['theater']
        sen = request.form['Senior']
        adult = request.form['Adult']
        children = request.form['Children']
        return render_template("paymentinfo.html", theater=theater, time=time)  
    except:
        return render_template("paymentinfo.html")  


if __name__ == '__main__':
    app.run()
