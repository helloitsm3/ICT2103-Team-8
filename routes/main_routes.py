from scripts.user import User
from flask import Blueprint, render_template, request, redirect, url_for, session

import scripts.scrapper.movie_controller as movie_controller

data = Blueprint("main_api", __name__)


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
    images = movie_controller.getCathayMainPosters()
    return render_template("main.html", images=images)


@data.route("/nowshowing/<moviename>", methods=["GET", "POST"])
def getNowShowingMovies(moviename):
    return moviename


@data.route("/login", methods=["GET", "POST"])
def do_admin_login():
    # After you enter the username and password and click submit the route will be invoked again as a POST request and both request.form['username'] and request.form['password'] will be set to the values entered by the user.

    if request.method == "POST":
        if not session.get("logged_in"):
            user = User()
            session["logged_in"] = user.fetchUser(
                request.form["username"], request.form["password"]
            )
            print("Successfully Logged In")
            return redirect(url_for("main_api.main"))
    else:
        if not session.get("logged_in"):
            return render_template("login.html")
        else:
            return redirect(url_for("main_api.main"))

    return redirect(url_for("main_api.main"))


@data.route("/logout")
def logout():
    if session.get("logged_in"):
        session["logged_in"] = False
        print("Successfully Logged out")

    return redirect(url_for("main_api.main"))


@data.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]

        if password == confirmpassword:
            user = User(username, email, password)
            print("Successfully created user {0}".format(username))
        else:
            print("Confirm Password is not the same as password")

        return redirect(url_for("main_api.main"))
    else:
        return render_template("register.html")