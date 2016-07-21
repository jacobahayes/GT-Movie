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

@app.route("/choosetheater")
def choose_theater():
    return render_template("choosetheater.html")

@app.route("/theaterresults")
def theaterresults():
    return render_template("theaterresults.html")

if __name__ == '__main__':
    app.run()
