from flask import Blueprint, render_template, request, redirect, url_for
import scripts.scrapper.movie_controller as movie_controller

data = Blueprint("main_api", __name__)

from flask import Flask, flash, redirect, render_template, request, session, abort


@data.route("/home")
def getHome():

    return '{"Data": "Welcome to the homepage"}'


@data.route("/nowshowing")
def getShowing():
    movies = movie_controller.getCathayMovie()

    return render_template("nowshowing.html", movies=movies)


@data.route("/moviedetail", methods=["POST"])
def getMovieDetail():
    poster = request.form["posterurl[]"]
    return render_template("moviedetail.html", poster=poster)


@data.route("/")
def main():
    if not session.get("logged_in"):
        return render_template("login.html")

    else:
        images = movie_controller.getCathayMainPosters()
        return render_template("main.html", images=images)


@data.route("/nowshowing/<moviename>", methods=["GET", "POST"])
def getNowShowingMovies(moviename):
    return moviename


@data.route("/login", methods=["POST"])
def do_admin_login():
    # After you enter the username and password and click submit the route will be invoked again as a POST request and both request.form['username'] and request.form['password'] will be set to the values entered by the user.
    if request.form["password"] == "password" and request.form["username"] == "admin":
        session["logged_in"] = True
    else:
        flash("wrong password!")
    return redirect(url_for("main_api.main"))

@data.route("/register")