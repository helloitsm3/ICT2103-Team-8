from flask import Blueprint, render_template, request, redirect, url_for

import scripts.scrapper.movie_controller as movie_controller

data = Blueprint("main_api", __name__)


@data.route("/home")
def getHome():
    return '{"Data": "Welcome to the homepage"}'

@data.route("/nowshowing")
def getShowing():
    movies = movie_controller.getCathayMovie()
    print(movies)
    
    return render_template("nowshowing.html", movies = movies)

@data.route("/moviedetail", methods=['POST'])
def getMovieDetail():
    poster = request.form['posterurl[]']
    return render_template("moviedetail.html", poster = poster)

@data.route("/")
def main():
    images = movie_controller.getCathayMainPosters()
    return render_template("main.html", images = images)

@data.route("/nowshowing/<moviename>", methods=['GET', 'POST'])
def getNowShowingMovies(moviename):
    return moviename