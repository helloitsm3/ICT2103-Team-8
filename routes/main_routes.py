from scripts.user import User
from datetime import datetime
from scripts.commands import *
from scripts.database import Database
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

import scripts.scrapper.movie_controller as movie_controller

data = Blueprint("main_api", __name__)


@data.route("/nowshowing")
def getShowing():
    movies = movie_controller.getCathayMovie()
    isLoggedIn = session.get("logged_in")

    return render_template("nowshowing.html", movies=movies, isLoggedIn=isLoggedIn)


@data.route("/moviedetail", methods=["POST"])
def getMovieDetail():
    poster = request.form["posterurl[]"]
    return render_template("moviedetail.html", poster=poster)


@data.route("/")
def main():
    images = movie_controller.getCathayMainPosters()
    isLoggedIn = session.get("logged_in")

    if isLoggedIn:
        user_data = session["user_data"]
        return render_template(
            "main.html", images=images, isLoggedIn=isLoggedIn, user_data=user_data
        )

    db = Database()
    # db.initMongoDB()
    # db.initMySQLTable()

    return render_template("main.html", images=images, isLoggedIn=isLoggedIn)


@data.route("/analytics")
def analytics():
    return render_template("main.html")


@data.route("/nowshowing/<moviename>", methods=["GET", "POST"])
def getNowShowingMovies(moviename):
    db = Database()
    current_db = db.getDB()
    isLoggedIn = session.get("logged_in")
    movie_details = []

    if "mongo" not in current_db:
        movie_det = db.fetchMovieByName(moviename)

        if len(movie_det) > 0:
            for movie_data in movie_det:
                movie_id = movie_data[0]
                ratings = (
                    float(db.getData(FETCH_RATINGS, movie_id)[0][0])
                    if db.getData(FETCH_RATINGS, movie_id)[0][0] != None
                    else movie_data[1]
                )
                movie_ratings = ratings
                movie_genre = movie_data[2]
                movie_country = movie_data[3]
                movie_director = movie_data[4]
                movie_runtime = movie_data[5]
                movie_poster_path = movie_data[6]
                movie_plot = movie_data[7]
                movie_title = movie_data[8]
                movie_release_date = datetime.strptime(
                    str(movie_data[13]), "%Y-%m-%d %H:%M:%S"
                )

                movie_details = [
                    {
                        "id": movie_id,
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
                        "casts": "Pedro Pascal, Carl Weathers, Emily Swallow, Nick Nolte, Rio Hackford, Misty Rosas",
                        "release_date": movie_release_date,
                    }
                ]

            session["current_movie"] = {"title": movie_title, "id": movie_id}

            reviews = db.getData(FETCH_ALL_REVIEW, movie_id)

            if isLoggedIn:
                return render_template(
                    "authenticated/auth_moviename.html",
                    movie_details=movie_details,
                    reviews=reviews,
                    isLoggedIn=isLoggedIn,
                )
            elif not isLoggedIn:
                return render_template(
                    "moviename.html", movie_details=movie_details, reviews=reviews
                )
            db.cleanConnection()
    else:
        # FOR ALL MONGO QUERIES
        movie_data = db.fetchMovieByName(moviename)
        movie_ratings = db.fetchMovieReviews(moviename)
        movie_reviews = ""
        movie_review_list = []

        for i in movie_data["reviews"]:
            author = ""
            review = ""
            rating = ""

            for key, values in i.items():
                if "author" in key:
                    author = values
                elif "review" in key:
                    review = values
                elif "rating" in key:
                    rating = values

            movie_reviews = (author, review, rating)
            movie_review_list.append(movie_reviews)

        try:
            mv_rate = movie_ratings["ratings_rounded"]
        except TypeError:
            mv_rate = "0"

        movie_details = [
            {
                "id": movie_data["_id"],
                "title": movie_data["title"],
                "poster_path": movie_data["poster"],
                "ratings": mv_rate,
                "reviews": movie_data["reviews"],
                "genre": "Family, Animation, Adventure, Comedy, Mystery",
                "country": "US",
                "run_time": movie_data["run_time"],
                "plot": movie_data["plot"],
                "overview": "",
                "original_language": "English",
                "writers": "Daniel Chong, Charlie Parisi, Quinne Larsen, Sooyeon Lee, Yvonne Hsuan Ho",
                "casts": "Pedro Pascal, Carl Weathers, Emily Swallow, Nick Nolte, Rio Hackford, Misty Rosas",
                "release_date": movie_data["release"],
            }
        ]

        if isLoggedIn:
            session["current_movie"] = movie_data["_id"]

            return render_template(
                "authenticated/auth_moviename.html",
                movie_details=movie_details,
                isLoggedIn=isLoggedIn,
                reviews=movie_review_list,
            )
        elif not isLoggedIn:
            return render_template(
                "moviename.html",
                movie_details=movie_details,
                reviews=movie_review_list,
            )

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
            if session["logged_in"]:
                flash("Successfully Logged In", "info")
                session["user_data"] = user.getUserData()
                return redirect(url_for("main_api.main"))
            else:
                flash("User login failed", "err")
                return render_template("login.html")
    else:
        if not session.get("logged_in"):
            return render_template("login.html")
        else:
            flash("You have already signed in", "info")
            return redirect(url_for("main_api.main"))


@data.route("/logout")
def logout():
    if session.get("logged_in"):
        session["logged_in"] = False
        flash("Successfully Logged out", "info")
        print("Successfully Logged out")

    return redirect(url_for("main_api.main"))


@data.route("/submitreview", methods=["POST", "GET"])
def submit_review():
    if request.method == "POST":
        isLoggedIn = session.get("logged_in")

        if isLoggedIn:
            db = Database()
            author_id = ""

            if "mongo" not in db.getDB():
                author_id = session.get("user_data")["id"]
            else:
                author_id = session.get("user_data")["username"]

            rating = request.form["movie_rating"]
            review = request.form["movie_review"]
            movie_title = session.get("current_movie")["title"]

            db = Database()
            db.userSubmitReview(author_id, movie_title, rating, review)
            db.cleanConnection()
            print("Successfully submitted review")
    return redirect(url_for("main_api.main"))


@data.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]

        if username != "" and email != "" and password != "":
            if password == confirmpassword:
                user = User()
                try:
                    user.createUser(username, email, password)
                    flash("Your account has been created successfully", "info")
                    print("Successfully created user {0}".format(username))
                    return redirect(url_for("main_api.main"))
                except:
                    flash("Username taken", "err")
                    print("Username taken")
                    return render_template("register.html")

            else:
                flash("Confirm Password is not the same as password", "err")
                return render_template("register.html")
        else:
            flash("Please enter all fields", "err")
            print("Please enter all fields")
            return render_template("register.html")

    else:
        return render_template("register.html")


@data.route("/search", methods=["GET", "POST"])
def search_movie():
    isLoggedIn = session.get("logged_in")
    if request.method == "POST":
        print(request.form["movieTitle"])
        db = Database()
        search_result = db.fetchFromMovieSearch(request.form["movieTitle"])
        return render_template(
            "search.html", results=search_result, isLoggedIn=isLoggedIn
        )
    else:
        db = Database()
        movie_top_ten = db.fetchTopTenMovieName()
        return render_template(
            "search.html", topTen=movie_top_ten, isLoggedIn=isLoggedIn
        )


@data.route("/wishlist", methods=["GET", "POST"])
def movie_wishlist():
    user = User()
    user_name = ""
    isLoggedIn = session.get("logged_in")

    if isLoggedIn:
        user_id = session["user_data"]["id"]
        user_name = user_id if user_id != "" else session["user_data"]["username"]

    # METHOD TO ADD MOVIE TO WISHLIST
    if request.method == "POST":
        movie_name = session["current_movie"]["title"]
        filtered_name = movie_name.lower().replace(" ", "-")

        user.addToWishlist(session["current_movie"], user_name)

        return redirect("/nowshowing/{0}".format(filtered_name))
    else:
        wish_list = user.getWishList(user_name)

        if isLoggedIn:
            return render_template(
                "wishlist.html", wishlist=wish_list, isLoggedIn=isLoggedIn
            )
        else:
            return redirect(url_for("main_api.main"))