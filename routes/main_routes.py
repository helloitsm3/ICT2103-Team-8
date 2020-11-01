from scripts.user import User
from datetime import datetime
from scripts.database import Database
from flask import Blueprint, render_template, request, redirect, url_for, session

import scripts.scrapper.movie_controller as movie_controller

data = Blueprint("main_api", __name__)


@data.route("/nowshowing")
def getShowing():
    movies = movie_controller.getCathayMovie()
    print(movies)

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
    movie_details = [
        {
            "title": moviename,
            "poster_path": "https://m.media-amazon.com/images/M/MV5BZTgyOWUyYTctMjQxNy00MDQ5LWFlMDQtODY2ZGEzYjIyYzRmXkEyXkFqcGdeQXVyMjg0MTI5NzQ@._V1_SX300.jpg",
            "ratings": "4.00",
            "genre": "Family, Animation, Adventure, Comedy, Mystery",
            "country": "US",
            "run_time": "108",
            "plot": "When Grizz, Panda, and Ice Bear's love of food trucks and viral videos went out of hand, it catches the attention of Agent Trout from the National Wildlife Control, who pledges to restore the “natural order” by separating them forever. Chased away from their home, the Bears embark on an epic road trip as they seek refuge in Canada, with their journey being filled with new friends, perilous obstacles, and huge parties. The risky journey also forces the Bears to face how they first met and became brothers, in order to keep their family bond from splitting apart.",
            "overview": "",
            "original_language": "English",
            "writers": "Daniel Chong, Charlie Parisi, Quinne Larsen, Sooyeon Lee, Yvonne Hsuan Ho",
            "casts": "",
            "release_date": datetime.strptime(
                "2020-06-25 00:00:00", "%Y-%m-%d %H:%M:%S"
            ),
        }
    ]

    db = Database()
    movie_det = db.fetchMovieByName(moviename)

    for movie_data in movie_det:
        movie_ratings = movie_data[1]
        movie_runtime = movie_data[6]
        movie_poster_path = movie_data[7]
        movie_plot = movie_data[8]
        movie_title = movie_data[9]
        movie_release_date = datetime.strptime(str(movie_data[14]), "%Y-%m-%d %H:%M:%S")

        movie_details = [
            {
                "title": movie_title,
                "poster_path": movie_poster_path,
                "ratings": movie_ratings,
                "genre": "Family, Animation, Adventure, Comedy, Mystery",
                "country": "US",
                "run_time": movie_runtime,
                "plot": movie_plot,
                "overview": "",
                "original_language": "English",
                "writers": "Daniel Chong, Charlie Parisi, Quinne Larsen, Sooyeon Lee, Yvonne Hsuan Ho",
                "casts": "",
                "release_date": movie_release_date,
            }
        ]

        return render_template("moviename.html", movie_details=movie_details)
    return "Error 404: Movie not found in our database"


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
        return render_template("register.html")
