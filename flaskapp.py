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
app.config['MYSQL_HOST'] = '127.6.155.2'
app.config['MYSQL_PORT'] = 3306
#app.config['MYSQL_HOST'] = '127.0.0.1'
#app.config['MYSQL_PORT'] = 3307
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
        hasSeen = False
        try:
            usern = str(request.form['usern'])
            movie = request.form["movie"]
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT giveReviews_UserHasSeenMovie ('"+usern+"','"+movie+"');")
            result = cursor.fetchone()[0]
            if result > 0 :
                hasSeen = True
            else: 
                hasSeen = False
            cursor.execute("SELECT util_GetAvgReviewRating ('"+movie+"');")
            avg = cursor.fetchone()[0]
            cursor.execute("CALL viewReviews_GetViewReviewsData ('"+movie+"');")
            result = cursor.fetchall()
            for r in result:
                reviews.append({'revs':r[0], 'ratings':r[1], 'comments':r[2]})
        except:
            return "Error"
        return render_template("review.html", hasSeen=hasSeen, usern=usern, avg=avg, reviews=reviews, movie=movie)

@app.route("/givereview", methods=['GET', 'POST'])
def give_review():
    if request.method == 'POST':
        try:
            usern = str(request.form['usern'])
            movie = request.form['movie']
        except Exception as e:
            return str(e)
        return render_template("givereview.html", usern=usern,  movie=movie)

@app.route("/procreview", methods=['POST'])
def proc_review():
    if request.method == 'POST':
        try:
            movie = request.form['movie']
            usern = str(request.form['usern'])
            rTitle = request.form['rtitle']
            rating = request.form['rating']
            comment = request.form['comment']
            print movie
            print usern
            print rTitle
            print rating
            print comment
            cursor = mysql.connection.cursor()
            cursor.execute("CALL givereviews_SubmitReview ('"+movie+"','"+rTitle+"','"+comment+"','"+rating+"','"+usern+"');")
            mysql.connection.commit()
            cursor.close()
            try:
                comment = request.form['comment']
            except:
                comment = "" 
            return redirect(url_for('movie', usern=usern, movie=movie), code=307)
        except Exception as e:
            return str(e)

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
                results.append({'name':str(t[0])+': '+str(t[1])+' '+str(t[2])+', '+str(t[3]), 'id':t[4]})
        except Exception as e:
            return str(e)
        return render_template("theaterresults.html", usern=usern, movie=movie, results=results)

@app.route("/selecttime", methods=['GET', 'POST'])
def selecttime():
    if request.method == 'POST':
        times = []
        try:
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
                cursor = mysql.connection.cursor()
                cursor.execute("CALL chooseTheater_SaveTheater ('"+theater+"','"+usern+"');")
                cursor.fetchall()
                cursor.close()
                mysql.connection.commit()
                print("Saved theater")
            except Exception as e:
                print(str(e))
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
    cards = []
    try:
        usern = str(request.form['usern'])
        time = request.form['time']
        movie = request.form['movie']
        theater = request.form['theater']
        sen = request.form['Senior']
        adult = request.form['Adult']
        children = request.form['Children']
        orderInfo = {'usern':usern, 
                'time':time,
                'movie':movie, 
                'theater': theater,
                'sen': sen,
                'adult':adult,
                'children':children}
        
        cursor = mysql.connection.cursor()
        cursor.execute("CALL buyTicket_GetSavedCards ('"+usern+"');")
        result = cursor.fetchall()
        print result
        for r in result:
            cards.append({'num':r[0], 'cvv':r[1], 'expdate':r[2], 'name':r[3]})

        return render_template("paymentinfo.html", orderInfo=orderInfo, cards=cards)  
    except Exception as e:
        return(str(e))

@app.route("/order", methods=['GET', 'POST'])                                                        
def order():                                                                                     
    try:
        theater = request.form['theater']
        usern = request.form['usern']
        movie = request.form['movie']
        adult = request.form['adult']
        sen = request.form['sen']
        child = request.form['children']
        time = request.form['time']
        cursor = mysql.connection.cursor()
        try:
            name = request.form['name']
            num = request.form['num']
            cvv = request.form['cvv']
            expdate = request.form['expdate']


            try:
                save = request.form['saveCard']
                stm = "CALL buyTicket_SubmitCard ('-1', '"+num+"', '"+expdate+"', '"+name+"', '"
                stm += cvv+"', '"+usern+"', '1');"
                cursor.execute(stm)
                print(stm)
            except:
                stm = "CALL buyTicket_SubmitCard ('-1', '"+num+"', '"+expdate+"', '"+name+"', '"
                stm += cvv+"', '"+usern+"', '0');"
                cursor.execute(stm)
                print(stm)

            cursor.fetchall()
        except Exception as e:
            print(e)
            try:
                num = request.form['savedcard']
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    statement = "CALL buyTicket_SubmitPurchase ('"+theater+"', '"+usern+"', '"+movie
    statement += "', '" +adult+"', '"+sen+"', '"+child+"', '"+time
    statement += "', '"+num+"');"
    print(statement)
    cursor.execute(statement)
    orderID = cursor.fetchall()[0][0]
    cursor.close()
    mysql.connection.commit()
    return render_template("order.html", usern=usern, orderNo=orderID)  

@app.route("/orderhistory", methods=['GET', 'POST'])                                                        
def orderhistory():                                                                                     
    if request.method == 'POST':
        orders = []
        try:
            usern = str(request.form['usern'])
            cursor = mysql.connection.cursor()
            cursor.execute("CALL orderHistory_GetOrderHIstory ('"+usern+"');")
            result = cursor.fetchall()
            for r in result:
                orders.append({'orderID':r[0],'movie':r[1],'status':r[2],'cost':r[3]})
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
    payments = []
    if request.method == 'POST':
        try:
            usern = str(request.form['usern'])
            cursor = mysql.connection.cursor()
            cursor.execute("CALL buyTicket_GetSavedCards ('"+usern+"')")
            result = cursor.fetchall()
            print result
            for r in result:
                payments.append({'carNum':r[0],'Name':r[3],'expDate':r[2]})
            try:
                payment = str(request.form['payment'])
                #payments = payments.remove(payment)
            except:
                pass
        except Exception as e:
            return str(e) 
        return render_template("preferredpayment.html", usern=usern, payments=payments)

@app.route("/preferredtheater", methods=['GET', 'POST'])
def preferredtheaters():
    if request.method == 'POST':
        theaters = []
        try:
            usern = str(request.form['usern'])
            cursor = mysql.connection.cursor()
            cursor.execute("CALL preferredTheaters_GetPreferredTheaters ('"+usern+"')")
            result = cursor.fetchall()
            for r in result:
                theaters.append({'Name':str(r[0]).upper(),'Address':str(r[1])+', '+str(r[2])+', '+str(r[3])+' '+str(r[4])})
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
