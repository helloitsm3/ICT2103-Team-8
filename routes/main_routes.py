from flask import Blueprint, render_template, request, redirect, url_for

import scripts.scrapper.movie_controller as movie_controller

data = Blueprint("main_api", __name__)


@data.route("/home")
def getHome():
    return '{"Data": "Welcome to the homepage"}'

@data.route("/nowshowing.html")
def getShowing():
    movies = movie_controller.getCathayMovie()
    return render_template("nowshowing.html", movies = movies)

@data.route("/")
def main():
    images = movie_controller.getCathayMainPosters()
    return render_template("main.html", images = images)