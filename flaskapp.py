import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
#from flask_mysqldb import MySQL
#
app = Flask(__name__)
#app.config.from_pyfile('flaskapp.cfg')
#app.config['MYSQL_USER'] = 'admingu2v3JA'
#app.config['MYSQL_PASSWORD'] = '4eaeGBP2ZlDh'
#app.config['MYSQL_DB'] = 'gtmovie'
#app.config['MYSQL_HOST'] = '127.6.155.2'
#app.config['MYSQL_PORT'] = 3306
#mysql = MySQL()
#mysql.init_app(app)

@app.route('/')
def index():
    #try:
    #    #conn = mysql.connect()
    #    cursor = mysql.connection.cursor()
    #    return("okay")
    #except Exception as e:
    #    return(str(e))


    #Query for login
    #if(query returns true) login
    #else tell user they're dumba nd to try again
    return render_template('index.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/nowplaying")
def nowplaying():
    return render_template("nowplaying.html", movies=["Captain America", "SpongeBob", "Cool", "Big Fish"])

@app.route("/me")
def me():
    return render_template("me.html")

@app.route("/movie", methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':
        try:
            movie = request.form['movie']
        except:
            movie = "Error"
        return render_template("movie.html", movie=movie)

@app.route("/overview")
def overview():
    return render_template("overview.html")

@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/givereview")
def give_review():
    return render_template("givereview.html")

@app.route("/choosetheater/<movie>", methods=['GET', 'POST'])
def choose_theater(movie):
    if request.method == 'GET':
        return render_template("choosetheater.html", movie=movie)

@app.route("/theaterresults", methods=['GET', 'POST'])
def theaterresults():
    if request.method == 'POST':
        try:
            search = request.form['Search']
            #do stuff with keyword
            results = search
        except:
            results = "ERROR"
        return render_template("theaterresults.html", movie=movie, results=results)

@app.route("/selecttime", methods=['GET', 'POST'])
def selecttime():
    if request.method == 'POST':
        #Do query with theater
        #Get times
        try:
            theater = request.form['theater']
            movie = request.form['movie']
            try:
                saveTheater = request.form['saveTheater']
                if (saveTheater == 'check'):
                    #SQL
                    print("Save theater")
            except:
                pass
        except:
            theater = "Error"
            movie = "Error"
        times = ['1:00pm', '3:00pm', '5:00pm', '7:00pm']
        return render_template("selecttime.html", movie=movie, times=times, theater=theater)

@app.route("/buyticket", methods=['GET', 'POST'])                                                        
def buyticket():                                                                                     
    if request.method == 'POST':
        try:
            theater = request.form['theater']
            movie = request.form['movie']
            time = request.form['time']
        except:
            theater = "Error"
            time = "Error"
            movie = "Error"
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return render_template("buyticket.html", nums=nums, movie=movie, theater=theater, time=time)

@app.route("/paymentinfo", methods=['GET', 'POST'])                                                        
def paymentinfo():                                                                                     
    try:
        time = request.form['time']
        movie = request.form['movie']
        theater = request.form['theater']
        sen = request.form['Senior']
        adult = request.form['Adult']
        children = request.form['Children']
        return render_template("paymentinfo.html", movie=movie, theater=theater, time=time)  
    except:
        return render_template("paymentinfo.html")  

@app.route("/order", methods=['GET', 'POST'])                                                        
def order():                                                                                     
    return render_template("order.html", orderNo='1234')  

if __name__ == '__main__':
    app.run()
