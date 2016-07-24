import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
app.config['MYSQL_USER'] = 'admingu2v3JA'
app.config['MYSQL_PASSWORD'] = '4eaeGBP2ZlDh'
app.config['MYSQL_DB'] = 'gtmovie'
#app.config['MYSQL_HOST'] = '127.6.155.2'
#app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3307
mysql = MySQL()
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        try:
            usern = request.form['usern']
            passw = request.form['password']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT gtmovie.login_AuthenticateUser(%s,%s) AS login_AuthenticateUser',(usern,passw)) 
            result = ''
            for record in cursor:
                result += str(record)
            cursor.close()
            if int(result[1]) == 1:
                return redirect(url_for("nowplaying", usern=usern), code=307)
            else:
                return render_template("index.html")
        except Exception as e:
            return(str(e))

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/nowplaying", methods=['GET', 'POST'])
def nowplaying():
    try:
        usern = request.form['usern']
        print str(usern)
    except Exception as e:
        return(str(e))
    cursor = mysql.connection.cursor()
    cursor.callproc('nowplaying_GetNowPlayingTitles')
    record = cursor.fetchall()
    result = []
    for r in record:
        result.append(str(r[0]))
    cursor.close()
    return render_template('nowplaying.html', usern=usern, movies=result)

@app.route("/me", methods=['GET', 'POST'])
def me():
    try:
        usern = request.form['usern']
    except Exception as e:
        return(str(e))
    return render_template("me.html", usern=usern)

@app.route("/movie", methods=['GET', 'POST'])
def movie():
    if request.method == 'GET':
        return render_template("movie.html", movie=movie)
    if request.method == 'POST':
        try:
            usern = request.form['usern']
            movie = str(request.form['movie'])
            print(str(usern))
            cursor = mysql.connection.cursor()
            cursor.execute("CALL movie_GetMovieData ('"+movie+"');")
            result = cursor.fetchone()
            cursor.close()
            release = str(result[0])
            MPAArating = str(result[1])
            length = str(result[2])
            genre = str(result[3])
            avgRating = str(result[4])
            data = {'movie': movie, 
                    'release': release,
                    'MPAArating': MPAArating,
                    'length': length,
                    'genre': genre,
                    'avgRating': avgRating}
        except Exception as e:
            return(str(e))
        return render_template("movie.html", usern=usern, data=data)

@app.route("/overview", methods=['GET', 'POST'])
def overview():
    if request.method == 'POST':
        data = {}
        try:
            usern = request.form['usern']
            movie = str(request.form['movie'])
            cursor = mysql.connection.cursor()
            cursor.execute("CALL overview_GetOVerviewData ('"+movie+"');")
            result = cursor.fetchone()
            cursor.close()
            data['syn'] = str(result[1])
            data['cast'] = {}
            data['cast']['actor1'] = str(result[2])
            data['cast']['role1'] = str(result[3])
            data['cast']['actor2'] = str(result[4])
            data['cast']['role2'] = str(result[5])
            data['cast']['actor3'] = str(result[6])
            data['cast']['role3'] = str(result[7])
            data['cast']['actor4'] = str(result[8])
            data['cast']['role4'] = str(result[9])
            data['cast']['actor5'] = str(result[10])
            data['cast']['role5'] = str(result[11])
        except Exception as e:
            return str(e)
        return render_template("overview.html", usern=usern, data=data, movie=movie)

@app.route("/review", methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        reviews = []
        comments = []
        try:
            usern = str(request.form['usern'])
            movie = request.form["movie"]
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT util_GetAvgReviewRating ('"+movie+"');")
            avg = cursor.fetchone()[0]
            cursor.execute("CALL viewReviews_GetViewReviewsData ('"+movie+"');")
            result = cursor.fetchall()
            print result
            for r in result:
                reviews.append(r[0])
                comments.append(r[2])
        except:
            return "Error"
        return render_template("review.html", usern=usern, avg=avg, reviews=reviews, movie=movie)

@app.route("/givereview", methods=['GET', 'POST'])
def give_review():
    if request.method == 'POST':
        try:
            usern = str(request.form['usern'])
            movie = request.form['movie']
        except:
            movie = "Error"
        return render_template("givereview.html", movie=movie)

@app.route("/procreview", methods=['POST'])
def proc_review():
        try:
            movie = request.form['movie']
            usern = str(request.form['usern'])
            rating = request.form['rating']
            try:
                comment = request.form['comment']
            except:
                comment = "" 
            return redirect(url_for('movie', usern=usern, movie=movie), code=307)
        except:
            return "Sorry failed"


@app.route("/choosetheater", methods=['GET', 'POST'])
def choose_theater():
    if request.method == 'GET':
        return render_template("choosetheater.html", movie=movie)
    if request.method == 'POST':
        theaters = []
        try:
            usern = request.form['usern']
            print(str(usern))
            movie = request.form['movie']
            cursor = mysql.connection.cursor()
            cursor.execute("CALL chooseTheater_GetSaved ('"+usern+"','"+movie+"');")
            result = cursor.fetchall()
            for r in result:
                theaters.append({'name':str(r[1]), 'id':str(r[0])})
        except Exception as e:
            return str(e)
        return render_template("choosetheater.html", theaters=theaters, usern=usern, movie=movie)

@app.route("/theaterresults", methods=['GET', 'POST'])
def theaterresults():
    if request.method == 'POST':
        results =[]
        try:
            usern = str(request.form['usern'])
            movie = request.form['movie']
            search = request.form['Search']
            cursor = mysql.connection.cursor()
            cursor.execute("CALL chooseTheater_searchTheater ('"+search+"','"+movie+"');")
            sResults = cursor.fetchall()
            for t in sResults:
                results.append(str(t[0])+': '+str(t[1])+' '+str(t[2])+', '+str(t[3]))
        except Exception as e:
            return str(e)
        return render_template("theaterresults.html", usern=usern, movie=movie, results=results)

@app.route("/selecttime", methods=['GET', 'POST'])
def selecttime():
    if request.method == 'POST':
        times = []
        try:
            theaterID ='1' # request.form['theater']
            usern = str(request.form['usern'])
            theater = request.form['theater']
            movie = request.form['movie']
            cursor = mysql.connection.cursor()
            cursor.execute("CALL selectTime_GetShowtimes ('"+movie+"','"+theater+"');")
            result = cursor.fetchall()
            print result
            for r in result:
                times.append(r[0])
            try:
                saveTheater = request.form['saveTheater']
                if (saveTheater == 'check'):
                    #SQL to save theater
                    print("Save theater")
            except:
                pass
        except Exception as e:
            return str(e)
        return render_template("selecttime.html", usern=usern, movie=movie, times=times, theater=theater)


@app.route("/buyticket", methods=['GET', 'POST'])                                                        
def buyticket():                                                                                     
    if request.method == 'POST':
        try:
            usern = str(request.form['usern'])
            theater = request.form['theater']
            movie = request.form['movie']
            time = request.form['time']
        except:
            return "Error"
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return render_template("buyticket.html", usern=usern, nums=nums, movie=movie, theater=theater, time=time)

@app.route("/paymentinfo", methods=['GET', 'POST'])                                                        
def paymentinfo():                                                                                     
    try:
        usern = str(request.form['usern'])
        time = request.form['time']
        movie = request.form['movie']
        theater = request.form['theater']
        sen = request.form['Senior']
        adult = request.form['Adult']
        children = request.form['Children']
        return render_template("paymentinfo.html", usern=usern, movie=movie, theater=theater, time=time)  
    except:
        return render_template("paymentinfo.html")  

@app.route("/order", methods=['GET', 'POST'])                                                        
def order():                                                                                     
    try:
        usern = str(request.form['usern'])
    except:
        return "Error"
    return render_template("order.html", orderNo='1234')  

@app.route("/orderhistory", methods=['GET', 'POST'])                                                        
def orderhistory():                                                                                     
    orders = ['1', '2', '3', '4']
    try:
        usern = str(request.form['usern'])
    except Exception as e:
        return(str(e)) 
    return render_template("orderhistory.html", usern=usern, orders=orders)  

@app.route("/orderdetail", methods=['GET', 'POST'])                                                        
def orderdetail():                                                                                     
    try:
        order = request.form['order']
        usern = str(request.form['usern'])
    except Exception as e:
        return(str(e)) 
    return render_template("orderdetail.html", usern=usern, order=order)  

@app.route("/preferredpayment", methods=['GET', 'POST'])
def preferredpayment():
    payments = ['1', '2', '3', '4']
    if request.method == 'POST':
        try:
            usern = str(request.form['usern'])
            try:
                payment = str(request.form['payment'])
                #payments = payments.remove(payment)
            except:
                pass
        except:
            return "Error"
        return render_template("preferredpayment.html", usern=usern, payments=payments)

@app.route("/preferredtheater", methods=['GET', 'POST'])
def preferredtheaters():
    if request.method == 'POST':
        try:
            usern = str(request.form['usern'])
            try:
                search = request.form['Search']
                #do stuff with keyword
                results = search
            except:
                results = "ERROR"
        except Exception as e:
            return(str(e)) 
        return render_template("preferredtheater.html", usern=usern)

if __name__ == '__main__':
    app.run()
